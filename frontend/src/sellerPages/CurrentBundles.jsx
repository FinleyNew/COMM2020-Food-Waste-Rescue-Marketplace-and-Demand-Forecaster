import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import './CurrentBundles.css'
import Company from "../assets/Company.png";
import Bundle from "../assets/BundleImage.png";
import axios from "axios";
function CurrentBundles() {

  const [categories, setCategories] = useState([]); //store the categories
  useEffect(() => { //to get all the categories at the start so they can be used throughout
    const API_URL = import.meta.env.VITE_API_URL;
    axios.get(`${API_URL}/api/v1/categories/`, {
    })
    .then(response => {
       setCategories(response.data); //store them in categories
       if (response.data.length > 0) {
      setBundleCategory(response.data[0].category_id); // ✅ real ID as default
      }
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching categories:", err);
        //alert("No data ");
    });
    },[])





  const API_URL = import.meta.env.VITE_API_URL;
  const [bundles, setBundles] = useState([]); //create state
  const [noBundles, setNoBundles] = useState(false);
  const [code, setCode] = useState("");
  const [updateBundle, setUpdateBundle] = useState(null);
  const navigate = useNavigate();
  
  const [bundleWeight, setBundleWeight] = useState("");
  
  const [bundlePrice,setBundlePrice] = useState("");
  const [bundleAllergens,setBundleAllergens] = useState("");
  const [bundleCategory, setBundleCategory] = useState("");
  const [numberAvailable, setNumberAvailable] = useState("");
  const [endTime, setEndTime] = useState("");
  const [startTime, setStartTime] = useState("");
  const token = localStorage.getItem('token');
  const payload = JSON.parse(atob(token.split('.')[1]));
  const today = new Date(); //need to get todays date to use to use the iso format
  const dateString = today.toISOString().split("T")[0]; // YYYY-MM-DD, removing the time to replace with the selected time
  const startDateTime = new Date(`${dateString}T${startTime}:00`); //creating new start time
  const endDateTime = new Date(`${dateString}T${endTime}:00`); //creating new end time
  const slots = Array.from({ length: 24 }, (_, i) => 
    { const start = i;
      const end = i + 1; 
      return `${String(start).padStart(2,"0")}:00 - ${String(end).padStart(2,"0")}:00`;
     });
  const [data, setForecastData] = useState({});


  useEffect(() => {
    const token = localStorage.getItem('token');
    axios.get(`${API_URL}/api/v1/bundles/me`, {
      headers:{
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
    .then(response => {

      const activeBundles = Array.isArray(response.data)
      ? response.data.filter(b => b.status !=="deleted")
      : [];


      setBundles(activeBundles);
      setNoBundles(activeBundles.length===0);
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching bundles:", err);
        alert("No data");
      });
  },[])



  const deleteBundle = (posting_id) => { //Function to delete bundles from backend
    console.log(typeof(posting_id));
    const token = localStorage.getItem('token');
    console.log(token);
    const postingID = posting_id;
    
    if (!window.confirm("Delete this bundle?")) return;
    
    axios.delete(`${API_URL}/api/v1/bundles/me/${postingID}`, {
      headers:{
        Authorization: `Bearer ${token}`,
      }
    })
    .then((response) => {
      console.log("Deleted:", response.data);
      setBundles(prev => prev.filter(b => b.posting_id !== posting_id));
  
      
    })
    .catch(err => { //Returns alert if an error occurs
         console.error("FULL ERROR:", err);

  if (err.response) {
    console.error("Backend error detail:", err.response.data);
    console.error("Status:", err.response.status);
  } else {
    console.error("No response from server:", err.message);
  }
    });
    
    
    
};

const handleUpdateBundle = (posting_id) => {
  const bundle = bundles.find(b => b.posting_id === posting_id);
   setBundleCategory(bundle.category.category_id);
  setUpdateBundle(posting_id);
};


const completeUpdateBundle = (posting_id) => {
  
    const categoryObject = categories.find(
      cat => cat.category_id === Number(bundleCategory) //create a catgeory object to upload both the name and the id at once
    );
    const data={};
    
    //Function to prevent extreme entry for bundle weight with an alert
    if(Number(bundleWeight)>10000 || Number(bundleWeight) <0){
      alert("Weight must be positive and less than 10,000");
      return;
    }
    //Alert for  extreme entry on number of available bundles
    else if(Number(numberAvailable)>1000 || Number(numberAvailable)<0){
      alert("Number available must be positive and less than 1000");
      return;
    }
    //Check for bundle price being too great or negative, sending an alert if so
    else if(Number(bundlePrice)>100 || Number(bundlePrice)<0){
      alert("Price must be positive and less than 100");
      return;
    }
    if(categoryObject) data.category = categoryObject;
    if(bundleAllergens) data.allergens = bundleAllergens;
    if(numberAvailable) data.available = Number(numberAvailable);
    if(bundlePrice) data.price = Number(bundlePrice);
    if(bundleWeight) data.weight = Number(bundleWeight);
    
    if(startTime){
      const today = new Date();
      const dateString = today.toISOString().split("T")[0];
      data.start_time = new Date(`${dateString}T${startTime}:00`).toISOString();
    }
     if (endTime) {
    const today = new Date();
    const dateString = today.toISOString().split("T")[0];
    data.end_time = new Date(`${dateString}T${endTime}:00`).toISOString();
  }

    console.log(data);
    console.log(categoryObject);
    
    axios.patch(`${API_URL}/api/v1/bundles/${posting_id}`, data ,{
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
    .then(() => {
      window.location.reload();
    })
      .catch(err => {
         if (err.response) {
    const backendData = err.response.data;
    console.error("Status code:", err.response.status);

    // If detail exists and is an array, print each error nicely
    if (backendData.detail && Array.isArray(backendData.detail)) {
      backendData.detail.forEach(d => {
        console.error(`Field: ${d.loc.join(" -> ")}, Message: ${d.msg}, Type: ${d.type}`);
      });
    } else {
      console.error("Backend response data:", backendData);
    }
  } else if (err.request) {
    console.error("No response from server:", err.request);
  } else {
    console.error("Error setting up request:", err.message);
  }
      }); 
    
};

const enterCode = (claim_code) => { //Function to return an entered code from the backend
  if (!window.confirm("Collect this bundle?")) return;
  const API_URL = import.meta.env.VITE_API_URL;
  const token = localStorage.getItem('token'); 

  axios.get(`${API_URL}/api/v1/reservations/collect/${claim_code}`, { //Fetches inputted tocken
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    }
  })
    .then(response => {
      console.log("Collected:", response.data);
      alert("Bundle collected");
    })
    .catch(err => console.error(err));
};


  return (
    <>
      <div className="currentBundles">
        {/* Initialises the navifation bar where sellers can move between pages */}
        <div className="pageHeading">
          <nav className="navRow">
            <Link to="/add-bundles" className="button"><b>Add Bundles</b></Link>
            <Link to="/analytics" className="button"><b>Analytics</b></Link>
            <Link to="/forecasts" className="button"><b>Forecasts</b></Link>
          </nav>
          <div className="textHeading">
            {/* Header to display the page name to the user */}
            <h1>Bundles</h1>
          </div>
        </div>
        <div className="rowBox">
          <div className="codeRow">
            <form onSubmit={(e) => {
                e.preventDefault();
                enterCode(code);
              }}>
                <input
                  id="enterCode"
                  type="text"
                  placeholder="Enter Code"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                />
                <button className="codeButton" type="submit">Collect</button>
              </form>
              <br></br>
          </div>
          <div className="searchRow">
            <p>Search for a Bundle: </p>
            <form onSubmit={(e) => {
                e.preventDefault();
                enterCode(code);
              }}>
                <input
                  id="enterCode"
                  type="text"
                  placeholder="Search"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                />
            </form>
            <br></br>
          </div>
        </div>
          {/* Columns structure for displaying bundle infomation */}
          <div className="mainBox">
            {bundles.map(bundle => ( //.map allows us to display
              <div key={bundle.posting_id} className="bundleEntry">
                {/* Final row bundle image */}
                <img
                  src={Bundle}
                  alt="Bundle"
                  className="bundleImage"
                />
                <div className="rowBox">
                  <h1>Bundle Name</h1>
                </div>
                <div className="rowBox">
                  <div className="textBox">
                    <p>Price: £{bundle.price_display}</p>
                    <p>Category: {bundle.category.name}</p>
                    <p>Available: {bundle.available}</p>
                    <p>Weight: {bundle.weight}g</p>
                    
                  </div>
                  {/* Holds the middle column data for the bundle entry */}
                  <div className="textBox">
                    <p>Allergens: {bundle.allergens} </p>
                    <p>Date to Collect: {bundle.formatted_date}</p>
                    <p>Time to Collect: {bundle.formatted_time_range}</p>
                    <p>Reserved: {bundle.reserved}</p>
                  </div>
                  <div className="columnBox">
                  {/* Contains company image and first column data */}
                    <div className="displayImage">
                      <img
                        src={Company}
                        alt="Company"
                        className="companyIcon"
                      />
                    </div>
                    {/* Button to delete bundles on click */}
                    <button className="updateButton" onClick={() => handleUpdateBundle(bundle.posting_id)}>
                        Update Bundle
                    </button>
                    <button className="deleteButton" onClick={() => deleteBundle(bundle.posting_id)}>
                        Delete Bundle
                    </button>
                  </div>
                </div>
                {updateBundle === bundle.posting_id&& ( 
                  <>
                      <div className="row">
                    {/* drop down for allergens */}
                    <label htmlFor="category">Enter Bundle Category : </label>
                  <select
                    name="category"
                    id="category"
                    value={bundleCategory}
                    onChange={(e) => setBundleCategory(e.target.value)}
                  >
                  {categories.map((cat) => (
                    <option key={cat.category_id} value={cat.category_id}>
                      {cat.name}
                    </option>
                  ))}
                  </select>
                  </div>


                  <div>
                <div className="row">
                  {/* Outputs an input box with a label asking for bundle allergen inputs */}
                  <label htmlFor="allergens">Enter Bundle Allergens : </label>
                  <input
                    id="allergens"
                    type="text"
                    value={bundleAllergens}
                    onChange={(e) => setBundleAllergens(e.target.value)}
                  />
                  </div>
                </div>


                  <div className="row">
                  {/* Makes an input box with a label to input the number of bundles to sell */}
                  <label htmlFor="numAvailable">Enter Number Available : </label>
                  <input
                    id="numAvailable"
                    type="number"
                    value={numberAvailable}
                    onChange={(e) => setNumberAvailable(e.target.value)}
                  />
              </div>

                  <div className="row">
                  {/* An input box with a label to input the bundle price */}
                  <label htmlFor="price">Enter Bundle Price : </label>
                  <input
                    id="price"
                    type="number"
                    value={bundlePrice}
                    onChange={(e) => setBundlePrice(e.target.value)}
                  />
                </div>

                  <div className="row">
                  {/* Outputs an input box with a label asking for bundle weight */}
                  <label htmlFor="weight">Enter Bundle Weight : </label>
                  <input
                    id="weight"
                    type="number"
                    value={bundleWeight}
                    onChange={(e) => setBundleWeight(e.target.value)}
                  />
                </div>

                  <div className="row">
                  {/* Outputs a drop down menu for the user to click a bundle collection time */}
                  <label htmlFor="collectionTime">Collection Time: </label>
                  {/* Divides the start and end time before saving them seperately */}
                  <select
                    id="collectionTime"
                    onChange={(e) => {
                      const[start,end] = e.target.value.split(" - ");
                      setStartTime(start);
                      setEndTime(end);
                    }}
                  >
                    {slots.map((slot,idx) =>(
                      <option key={idx} value={slot}>
                        {slot}
                      </option>
                    ))}
                  </select>
                    {/* Button to add bundles when clicked and forecast the data */}
                </div>
                <button className="boxButton" onClick={() => completeUpdateBundle(bundle.posting_id)}>Confirm Update Bundle</button>
                <button className="boxButton" onClick={() => setUpdateBundle(null)}>Cancel Update</button>
                </>
                
                  
                
              )}
              
              

              

                

              </div>
          
            ))}
          </div>
          {noBundles && (
          <p style={{color:"red"}}>
                      No bundles
                  </p>)}
        </div>
    </>
  );
}
//exports the component so it can be imported in other files
export default CurrentBundles;
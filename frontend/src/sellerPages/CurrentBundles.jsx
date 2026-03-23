import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import './CurrentBundles.css'
import Company from "../assets/Company.png";
import Bundle from "../assets/BundleImage.png";
import axios from "axios";
function CurrentBundles() {
  const [Popup, setPopup] = useState(false);
  const [collectPopup, setCollectPopup] = useState(false);

  const [categories, setCategories] = useState([]); //store the categories
  useEffect(() => { //to get all the categories at the start so they can be used throughout
    const API_URL = import.meta.env.VITE_API_URL;
    axios.get(`${API_URL}/api/v1/categories/`, {
    })
    .then(response => {
       setCategories(response.data); //store them in categories
       if (response.data.length > 0) {
      setBundleCategory(response.data[0].category_id); // real ID as default
      }
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching categories:", err);
        //alert("No data ");
    });
    },[])





  const API_URL = import.meta.env.VITE_API_URL;
  const [forecasts, setForecasts] = useState([]);
  const [bundles, setBundles] = useState([]); //create state
  const [noBundles, setNoBundles] = useState(false);
  const [code, setCode] = useState("");
  const [updateBundle, setUpdateBundle] = useState(null);
  const [deleteID, setDeleteID] = useState(null);
  const navigate = useNavigate();
  const [openReply, setOpenReply] = useState(null); 
  const [replyText, setReplyText] = useState({});  
  const [bundleWeight, setBundleWeight] = useState("");
  const [viewReports, setViewReports] = useState("");
  const [reports, setReports] = useState([]);
  const [bundlePrice,setBundlePrice] = useState("");
  const [bundleAllergens,setBundleAllergens] = useState("");
  const [bundleCategory, setBundleCategory] = useState("");
  const [numberAvailable, setNumberAvailable] = useState("");
  const [endTime, setEndTime] = useState("");
  const [startTime, setStartTime] = useState("");
  const [description, setDescription] = useState("")
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
  const [noForecasts, setNoForecasts] = useState(false);

  useEffect(() => {
      const token = localStorage.getItem('token');
  
      axios.get(`${API_URL}/api/v1/forecasts/me`, { //Fetch data for the user
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      })
        .then(response => {
          //setForecasts(response.data); // data is likely an array
          //setAnalytics(response.data);
        if (response.data.length === 0) {
            setNoForecasts(true);
          } else {
            setForecasts(response.data);
            setNoForecasts(false);
          }
        })
        .catch(err => { //Returns alert if an error occurs
          console.error("Error fetching forecasts:", err);
          alert("No data");
        });
    }, []);

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
  function openPopup() {
    setPopup(true); //if variable is true then popUp needs to be opened 
  }
  function closePopup() {
    setPopup(false); //if variable is false then popUp needs to be closed
  }



  const confirmDelete = (posting_id) => { //Function to delete bundles from backend
    console.log(typeof(posting_id));
    const token = localStorage.getItem('token');
    console.log(token);
    const postingID = posting_id;
    const API_URL = import.meta.env.VITE_API_URL;
    axios.delete(`${API_URL}/api/v1/bundles/me/${postingID}`, {
      headers:{
        Authorization: `Bearer ${token}`,
      }
    })
    .then((response) => {
      console.log("Deleted:", response.data);
      setBundles(prev => prev.filter(b => b.posting_id !== posting_id));
      setDeleteID(null);
    })
    .catch(err => { //Returns alert if an error occurs
         console.error("FULL ERROR:", err);
         setDeleteID(null);
        alert("Delete Failed");

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

const enterCode = (inputCode) => { //Function to return an entered code from the backend
  setCollectPopup(true);
};

const confirmCollect = () => {
  const API_URL = import.meta.env.VITE_API_URL;
  const token = localStorage.getItem('token'); 

  axios.get(`${API_URL}/api/v1/reservations/collect/${code}`, { //Fetches inputted tocken
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    }
  })
    .then(response => {
      console.log("Collected:", response.data);
      setCollectPopup(false);
      setCode("")
    })
    .catch(err => {
      console.error(err);
      alert("Collection Failed");
      setCollectPopup(false);
    });
};


const handleViewReports = (bundle_id)  => {
  const token = localStorage.getItem('token');
  const API_URL = import.meta.env.VITE_API_URL;

  axios.get(`${API_URL}/api/v1/reports/seller/${bundle_id}`, {  
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  })                                                      
  .then(response => {
    console.log("response created");
    console.log(response.data);
    setReports(response.data);
    setViewReports(bundle_id);
  });
}

const submitReply = (issue_id) => {
  const token = localStorage.getItem('token');
  const API_URL = import.meta.env.VITE_API_URL;

  axios.patch(`${API_URL}/api/v1/reports/${issue_id}/${replyText[issue_id]}`,
    {},  // empty body
    { headers: { "Authorization": `Bearer ${token}` }}  // config goes here
  )
  .then(() => {
    alert("Response sent!");
    setOpenReply(null);
    setReplyText(prev => ({ ...prev, [issue_id]: "" }));  // use issue_id not report_id
    window.location.reload();
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
                  <h1>{bundle.seller.name}</h1>
                </div>
                <div className="rowBox">
                  <div className="textBox">
                    <p>Price: £{bundle.price_display}</p>
                    <p>Category: {bundle.category.name}</p>
                    <p>Available: {bundle.available}</p>
                    <p>Weight: {bundle.weight}g</p>
                    <p>Description: {bundle.contents}</p>
                    <p>Discount: {bundle.discount_percent}</p>
                    <div className="forecastColumn">
                      {(() => {
                      const forecast = forecasts.find(f => f.posting_id === bundle.posting_id);
                      return forecast ? (
                        <>
                          <h2>Forecast:</h2>
                          <p>Predicted Reservations: {forecast.predicted_reservations}</p>
                          <p>Predicted No-show Probability: {forecast.predicted_no_show_prob}</p>
                        </>
                        ) : (
                         <p>No Forecast Available</p>
                        );
                    })()}
                    </div>
                  </div>
                  {/* Holds the middle column data for the bundle entry */}
                  <div className="textBox">
                    <p>Reserved: {bundle.reserved}</p>
                    <p>Allergens: {bundle.allergens} </p>
                    <p>Date to Collect: {bundle.formatted_date}</p>
                    <p>Time to Collect: {bundle.formatted_time_range}</p>
                    <div className="buttonColumn">
                      <button className="updateButton" onClick={() => handleUpdateBundle(bundle.posting_id)}>
                          Update Bundle
                      </button>
                      {/* Button to delete bundles on click */}
                      <button className="deleteButton" onClick={() => setDeleteID(bundle.posting_id)}>
                          Delete Bundle
                      </button>
                    </div>
                  </div>
                  <div className="columnBox">
                  {/* Contains company image and first column data */}
                    <div className="displayImage">
                      <img
                        src={bundle.seller.logo_url}
                        alt="Company"
                        className="companyIcon"
                      />
                    </div>
                  </div>
                </div>
                {deleteID === bundle.posting_id && (
                  <div className="popupRegister open-popupRegister">
                    <div className="updateBox">
                      <h2>Would you like to delete this bundle?</h2>
                      <div className="rowBox">
                        <button className="deleteBundleButton" onClick={() => confirmDelete(bundle.posting_id)}>Delete</button>
                        <button className="deleteBundleButton" onClick={() => setDeleteID(null)}>Cancel</button>
                      </div>
                    </div>
                  </div>
                )}
                {updateBundle === bundle.posting_id && ( 
                  <>
                  <div className="popupRegister open-popupRegister">
                    <div className="updateBox">
                      <h1>Update Details</h1>
                      <br></br>
                          <div className="row">
                        {/* drop down for allergens */}
                        <label htmlFor="category">Enter Bundle Category : </label>
                        <select
                          name="category"
                          id="category"
                          value={bundleCategory}
                          onChange={(e) => setBundleCategory(e.target.value)}
                        >
                        {/* List of options fo the user to choose from the menu */}
                        <option value="">Select Category</option>
                        <option value="Baked Goods">Baked Goods</option>
                        <option value="Fruit">Fruit</option>
                        <option value="Vegetables">Vegetables</option>
                        <option value="Meat">Meat</option>
                        <option value="Seafood">Seafood</option>
                        <option value="Snacks">Snacks</option>
                        <option value="Dairy">Dairy</option>
                        <option value="Drinks">Drinks</option>
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
                    <br></br>

                    <div className="row">
                      </div>
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
                      <label htmlFor="price">Enter Bundle Price: </label>
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
                    <div className="rowBox">
                      <button className="button" onClick={() => completeUpdateBundle(bundle.posting_id)}>Confirm Update Bundle</button>
                      <button className="button" onClick={() => setUpdateBundle(null)}>Cancel Update</button>
                    </div>
                  </div>
                  </div>
                </>
              )}
              
              {viewReports === bundle.posting_id && (
              <>
                {reports.map(report => (
                  <div key={report.issue_id}>
                  <p>Description: {report.description}</p>
                  <p>Status: {report.status}</p>
                  <p>Seller Response: {report.seller_response}</p>

                <button onClick={() => setOpenReply(openReply === report.issue_id ? null : report.issue_id)}>
                  {openReply === report.issue_id ? "Cancel" : "Respond"}
                </button>

                {openReply === report.issue_id && (
                  <div>
                  <input
                    value={replyText[report.issue_id] || ""}
                    onChange={(e) => setReplyText(prev => ({ ...prev, [report.issue_id]: e.target.value }))}
                    placeholder="Type Response"
                  />
                <br>
                </br>
                <button onClick={() => submitReply(report.issue_id)}>Submit Response</button>
                  </div>
                )}
              </div>
              ))}
              </>
            )}
              </div>
          
            ))}
          </div>
          {collectPopup && (
            <div className="popupRegister open-popupRegister">
              <div className="updateBox">
                <h1>Confirm Bundle Collect</h1>
                <h2>Are you sure you want to collect the bundle?</h2>
                <div className="collectRow">
                  <button className="deleteBundleButton" onClick={confirmCollect}>Confirm</button>
                  <button className="deleteBundleButton" onClick={() => setCollectPopup(false)}>Back</button>
                </div>
              </div>
            </div>
          )}
          {noBundles && (
          <div className="mainBox">
            <p className="errorBox" style={{color:"red"}}>
                No bundles
            </p>
          </div>
          )}
        </div>
    </>
  );
}
//exports the component so it can be imported in other files
export default CurrentBundles;
import { Routes, Route, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import './AddBundles.css'
import axios from "axios";

function AddBundles() {


  const [categories, setCategories] = useState([]); //store the categories
  useEffect(() => { //to get all the categories at the start so they can be used throughout
      
    axios.get(`${API_URL}/api/v1/categories/`, {
    })
    .then(response => {
       setCategories(response.data); //store them in categories
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching categories:", err);
        //alert("No data ");
    });
    },[])

    



  const API_URL = import.meta.env.VITE_API_URL;
  const [bundleWeight, setBundleWeight] = useState("0");
  
  
  const [bundleAllergens,setBundleAllergens] = useState("");
  const [bundleCategory, setBundleCategory] = useState(1);
 
  const [bundlePrice,setBundlePrice] = useState("");
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
  function addBundle(){
    //Initialise data to be sent to the backend
    const categoryObject = categories.find(
      cat => cat.category_id === Number(bundleCategory) //create a catgeory object to upload both the name and the id at once
    );

    const data = {
      user_id: Number(payload.sub),
      category: categoryObject,
      allergens: bundleAllergens,
      available: Number(numberAvailable),
      price: Number(bundlePrice),
      weight: Number(bundleWeight),
      start_time: startDateTime.toISOString(),
      end_time: endDateTime.toISOString()
    };
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
    console.log(data);
    console.log(categoryObject);
    console.log(bundleCategory);
    
    axios.post(`${API_URL}/api/v1/bundles/`, data ,{
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
      
  }

  

    
   


  function forecastData(){
    const API_URL = import.meta.env.VITE_API_URL;
    const categoryObject = categories.find(
      cat => cat.category_id === Number(bundleCategory) //create a catgeory object to upload both the name and the id at once
    );
    //Data to be used in th forecast
    const data = {
      user_id: Number(payload.sub),
      category: categoryObject,
      allergens: bundleAllergens,
      available: Number(numberAvailable),
      price: Number(bundlePrice),
      weight: Number(bundleWeight),
      start_time: startDateTime.toISOString(),
      end_time: endDateTime.toISOString()
    };
    console.log(data);
    //Checks bundle weight to be forecasted isn't extreme
    if(Number(bundleWeight)>10000 || Number(bundleWeight) <0){
      alert("Weight must be positive and less than 10,000");
      return;
    }
    //Alert for if the number available is too great or less than 0
    else if(Number(numberAvailable)>1000 || Number(numberAvailable)<0){
      alert("Number available must be positive and less than 1000");
      return;
    }
    //Sends an alert if the price is too extreme or less than zero
    else if(Number(bundlePrice)>100 || Number(bundlePrice)<0){
      alert("Price must be positive and less than 100");
      return;
    }

    axios.post(`${API_URL}/api/v1/forecasts/`, data, {
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
      }
    })
    .then(response => {
      setForecastData(response.data);
    })
    .catch(err => {
      console.error("Backend error detail:", err.response?.data); // <-- add this console.error("Status:", err.response?.status);
      console.error("Status:", err.response?.status);
    })
  }
  return (
    <>
      {/* Initialises the navifation bar where sellers can move between pages */}
      <div className="addBundles">
        <div className="pageHeading">
          <nav className="navRow">
            <Link to="/current-bundles" className="button"><b>Current Bundles</b></Link>
            <Link to="/analytics" className="button"><b>Analytics</b></Link>
            <Link to="/forecasts" className="button"><b>Forecasts</b></Link>
          </nav>
          <div className="textHeading">
            <h1>Add Bundles</h1> 
          </div>
        </div>
        <div className="mainBox">
          <div className="bundleEntry"> 
            {/* Displays a header which states the name of the current page */}
            <h1>Add Bundles</h1>
              <div className="textBox">
                <div className="row">
                  {/* Creates a drop down menu for the user to click a bundle category */}
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
              </div>
              <div className="textBox">
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
              <div className="textBox">
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
              </div>
              <div className="textBox">
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
              </div>
              <div className="textBox">
                <div className="row">
                  {/* Outputs an input box with a label asking for bundle weight */}
                  <label htmlFor="weight">Enter Bundle Weight (grams): </label>
                  <input
                    id="weight"
                    type="number"
                    value={bundleWeight}
                    onChange={(e) => setBundleWeight(e.target.value)}
                  />
                </div>
              </div>
              <div className="textBox">
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
              </div>
              <div className="textBox">
                <div className="row">
                  <button className="boxButton" onClick={addBundle}>Add Bundle</button>
                  <button className="boxButton" onClick={forecastData}>Forecast Data</button>
                </div>
              </div>
            </div>
          </div>
          <div className="mainBox">
            <div className="forecastEntry">
              <h1>Forecasting</h1>
              <h4>Predicted Reservations: {data.predicted_reservations}</h4>
              <h4>Predicted No Show Probability: {data.predicted_no_show_prob}</h4>
            </div>
          </div>
      </div>
    </>
  );
}
//exports the component so it can be imported in other files
export default AddBundles;

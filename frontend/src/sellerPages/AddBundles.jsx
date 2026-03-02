import { Routes, Route, Link } from "react-router-dom";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function AddBundles() {
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
  function addBundle(){
    //Initialise data to be sent to the backend
    const data = {
      user_id: Number(payload.sub),
      category: bundleCategory,
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
    fetch("http://127.0.0.1:8000/api/v1/bundles/", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });
  }
  function forecastData(){
    //Data to be used in th forecast
    const data = {
      user_id: Number(payload.sub),
      category: bundleCategory,
      allergens: bundleAllergens,
      available: Number(numberAvailable),
      price: Number(bundlePrice),
      weight: Number(bundleWeight),
      start_time: startDateTime.toISOString(),
      end_time: endDateTime.toISOString()
    };
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
    //Sends forecast data to the backend as a POST request
    fetch("http://127.0.0.1:8000/api/v1/forecasts/", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    })
    .then(res => {
      if(!res.ok){
        throw new Error(`Server Error: ${res.status}`);
      }
      return res.json();
    })
    .then(data => {
      setForecastData(data);
    })
    //Alerts upon an error
    .catch(err => {
      console.error("Error fetching bundles ",err);
      alert("No data")
    })
    
  }
  
  return (
    <>
    {/* Initialises the navifation bar where sellers can move between pages */}
      <nav className="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/current-bundles" className="button"><b>Current Bundles</b></Link>
        <Link to="/analytics" className="button"><b>Analytics</b></Link>
        <Link to="/forecasts" className="button"><b>Forecasts</b></Link>
      </nav>
    <div className="centreBox">
      <div className="centreItems">
          {/* Displays a header which states the name of the current page */}
        <h1 className="headline">Add Bundles</h1>

        <section>  
          <div className="textBlock">
            {/* Creates a drop down menu for the user to click a bundle category */}
            <label htmlFor="category">Enter Bundle Category :</label>

            <select
              name="category"
              id="category"
              value={bundleCategory}
              onChange={(e) => setBundleCategory(e.target.value)}
            >
            {/* List of options fo the user to choose from the menu */}
            <option value="">Select Category</option>
            <option value="baked_goods">Baked Goods</option>
            <option value="fruit">Fruit</option>
            <option value="vegetables">Vegetables</option>
            <option value="meat">Meat</option>
            <option value="seafood">Seafood</option>
            <option value="SNACKS">Snacks</option>
            <option value="dairy">Dairy</option>
            <option value="drinks">Drinks</option>
            </select>

            {/* Creates a space in the page */}         
            <br></br>

            {/* Outputs an input box with a label asking for bundle allergen inputs */}
            <label htmlFor="allergens">Enter Bundle Allergens :</label>
            <input
              id="allergens"
              type="text"
              value={bundleAllergens}
              onChange={(e) => setBundleAllergens(e.target.value)}
            />
            {/* Creates a space in the page between boxes */}
            <br></br>

            {/* Makes an input box with a label to input the number of bundles to sell */}
            <label htmlFor="numAvailable">Enter Number Available :</label>
            <input
              id="numAvailable"
              type="number"
              value={numberAvailable}
              onChange={(e) => setNumberAvailable(e.target.value)}
            />
            {/* Creates a space in the page between boxes */}
            <br></br>

            {/* An input box with a label to input the bundle price */}
            <label htmlFor="price">Enter Bundle Price :</label>
            <input
              id="price"
              type="number"
              value={bundlePrice}
              onChange={(e) => setBundlePrice(e.target.value)}
            />
            {/* Creates a space in the page between boxes */}
            <br></br>
            
            {/* Outputs an input box with a label asking for bundle weight */}
            <label htmlFor="weight">Enter Bundle Weight :</label>
            <input
              id="weight"
              type="number"
              value={bundleWeight}
              onChange={(e) => setBundleWeight(e.target.value)}
            />
            {/* Creates a space in the page between boxes */}
            <br></br>
            
          {/* Outputs a drop down menu for the user to click a bundle collection time */}
          <label htmlFor="collectionTime">Collection Time</label>
          <select
            id="collectionTime"
            onChange={(e) => { {/* Divides the start and end time before saving them seperately */}
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
            <br></br>
            {/* Button to add bundles when clicked and forecast the data */}
            <button onClick={addBundle}>Add Bundle</button>
            <br></br>
            <button onClick={forecastData}>Forecast Data</button>
          </div>
        </section>
        {/* Section with forecast data on added bundle with probabilities */}
        <section>
          <h4>Forecasts</h4>
              <p>Predicted Reservations : {data.predicted_reservations}</p>
              <p>No Show Probability : {data.predicted_no_show_prob}</p>
        </section>
      </div>
    </div>
    </>
  );
}
//exports the component so it can be imported in other files
export default AddBundles;

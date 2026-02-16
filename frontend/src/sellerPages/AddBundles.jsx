import { Routes, Route, Link } from "react-router-dom";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function AddBundles() {
  
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
  const [data, setForecastData] = useState([]);
  function addBundle(){
    const data = {
      user_id: Number(payload.sub),
      category: bundleCategory,
      allergens: bundleAllergens,
      available: Number(numberAvailable),
      price: Number(bundlePrice),
      start_time: startDateTime.toISOString(),
      end_time: endDateTime.toISOString()
    };
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
    const data = {
      
      user_id: Number(payload.sub),
      category: bundleCategory,
      allergens: bundleAllergens,
      available: Number(numberAvailable),
      price: Number(bundlePrice),
      start_time: startDateTime.toISOString(),
      end_time: endDateTime.toISOString()
    };
    console.log(data);
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
    .catch(err => {
      console.error("Error fetching bundles ",err);
      alert("No data")
    })
    
  }
  
  return (
    <>
      <nav className="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/current-bundles" className="button"><b>Current Bundles</b></Link>
        <Link to="/analytics" className="button"><b>Analytics</b></Link>
        <Link to="/forecasts" className="button"><b>Forecasts</b></Link>
      </nav>

      <h1 className="headline">Add Bundles</h1>

      <section>
        
        

        
        <div className="textBlock">
          <label htmlFor="category">Enter Bundle Category :</label>

          <select
            name="category"
            id="category"
            value={bundleCategory}
            onChange={(e) => setBundleCategory(e.target.value)}
          >
          <option value="">Select category</option>
          <option value="baked_goods">Baked Goods</option>
          <option value="fruit">Fruit</option>
          <option value="vegetables">Vegetables</option>
          <option value="meat">Meat</option>
          
          <option value="seafood">Seafood</option>
          <option value="SNACKS">Snacks</option>
          <option value="dairy">Dairy</option>
          <option value="drinks">Drinks</option>
          </select>



          {/*
          <label htmlFor="category">Enter Bundle Category :</label>
          <input
            id="category"
            type="text"
            value={bundleCategory}
            onChange={(e) => setBundleCategory(e.target.value)}
          />
          
          */ }
          
          <br></br>


          <label htmlFor="allergens">Enter Bundle Allergens :</label>
          <input
            id="allergens"
            type="text"
            value={bundleAllergens}
            onChange={(e) => setBundleAllergens(e.target.value)}
          />
          <br></br>




          <label htmlFor="numAvailable">Enter Number Available :</label>
          <input
            id="numAvailable"
            type="number"
            value={numberAvailable}
            onChange={(e) => setNumberAvailable(e.target.value)}
          />
          <br></br>


          <label htmlFor="price">Enter Bundle Price :</label>
          <input
            id="price"
            type="number"
            value={bundlePrice}
            onChange={(e) => setBundlePrice(e.target.value)}
          />
          <br></br>

          

         <label htmlFor="collectionTime">Collection Time</label>
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

          


          
          {/*
          <label htmlFor="startTime">Enter Start Timel :</label>
          <input
            id="startTime"
            type="datetime-local"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
          />
          <br></br>

          
      

          <label htmlFor="endTime">Enter End Time :</label>
          <input
            id="endTime"
            type="datetime-local"
            value={endTime}
            onChange={(e) => setEndTime(e.target.value)}
          />
          <br></br>
          
          */}
          <br></br>
          <button onClick={addBundle}>Add Bundle</button>
          <br></br>
          <button onClick={forecastData}>Forecast Data</button>
        </div>
      </section>
    </>
  );
}

export default AddBundles;

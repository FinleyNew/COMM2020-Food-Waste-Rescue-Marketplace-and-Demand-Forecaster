import { Routes, Route, Link } from "react-router-dom";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function AddBundles() {
  const [bundleName, setBundleName] = useState("");
  const [location, setLocation] = useState("");
  const [collectionTime, setCollectionTime] = useState("");
  const [bundlePrice,setBundlePrice] = useState("");
  const [bundleAllergens,setBundleAllergens] = useState("");
  const [bundleCategory, setBundleCategory] = useState("");
  const [numberAvailable, setNumberAvailable] = useState("");
  const [endTime, setEndTime] = useState("");
  const [startTime, setStartTime] = useState("");
  const token = localStorage.getItem('token');
  function addBundle(){
    const data = {
      //bundleName: bundleName,
      //location: location,
      //collectionTime: collectionTime
      user_id: token,
      category: bundleCategory,
      allergens: bundleAllergens,
      available: numberAvailable,
      price: bundlePrice,
      start_time: startTime,
      end_time: endTime
    };
    
    fetch("http://127.0.0.1:8000/api/v1/bundles/", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });
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
          <label htmlFor="price">Enter Bundle Price :</label>
          <input
            id="price"
            type="text"
            value={bundlePrice}
            onChange={(e) => setBundlePrice(e.target.value)}
          />
          <br></br>

          <label htmlFor="allergens">Enter Bundle Allergens :</label>
          <input
            id="allergens"
            type="text"
            value={bundleAllergens}
            onChange={(e) => setBundleAllergens(e.target.value)}
          />
          <br></br>


          <label htmlFor="category">Enter Bundle Category :</label>
          <input
            id="category"
            type="text"
            value={bundleCategory}
            onChange={(e) => setBundleCategory(e.target.value)}
          />
          <br></br>


          <label htmlFor="numAvailable">Enter Number Available :</label>
          <input
            id="numAvailable"
            type="text"
            value={numberAvailable}
            onChange={(e) => setNumberAvailable(e.target.value)}
          />
          <br></br>

          <label htmlFor="startTime">Enter Start Time :</label>
          <input
            id="startTime"
            type="text"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
          />
          <br></br>


          <label htmlFor="endTime">Enter End Time :</label>
          <input
            id="endTime"
            type="text"
            value={endTime}
            onChange={(e) => setEndTime(e.target.value)}
          />
          <br></br>
          <button onClick={addBundle}>Add Bundle</button>

        </div>
      </section>
    </>
  );
}

export default AddBundles;

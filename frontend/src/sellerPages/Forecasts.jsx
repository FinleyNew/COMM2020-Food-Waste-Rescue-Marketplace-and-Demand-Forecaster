import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";

function Forecasts() {
  const [forecasts, setForecasts] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('token');

    fetch("http://127.0.0.1:8000/api/v1/forecasts/me", {
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
      .then(res => res.json())
      .then(data => {
        setForecasts(data); // data is likely an array
      })
      .catch(err => {
        console.error("Error fetching forecasts:", err);
        alert("No data");
      });
  }, []);

  return (
    <>
      <nav>
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/current-bundles" className="button"><b>Current Bundles</b></Link>
        <Link to="/add-bundles" className="button"><b>Add Bundles</b></Link>
        <Link to="/analytics" className="button"><b>Analytics</b></Link>
      </nav>

      <section>
        {forecasts.length === 0 ? (
          <p>Loading forecasts...</p>
        ) : (
          forecasts.map(forecast => (
            <div key={forecast.forecast_id}>              <p>Predicted Reservations: {forecast.predicted_reservations}</p>
              <p>Predicted No-show Probability: {forecast.predicted_no_show_prob}</p>
              <p>User ID: {forecast.user_id}</p>
              <p></p>
              <hr />
            </div>
          ))
        )}
      </section>
      {/*
        <section>
        <div className="textBlock">
          <form>
            <p>Seller ID:</p>
              <input type="text"/>
            <p>Number of Bundles:</p>
              <input type="text"/>
            <p>Day of the Week:</p>
              <input type="text"/>
            <p>Pickup Time Window:</p>
              <input type="text"/>
            <p>Product Type:</p>
              <input type="text"/>
            <p>Price:</p>
              <input type="text"/>
              <br></br>
              <br></br>
            <button className="button" type="submit">Generate</button>
          </form>
        </div>

      </section>
      */}
      
    </>
  );
}

export default Forecasts;

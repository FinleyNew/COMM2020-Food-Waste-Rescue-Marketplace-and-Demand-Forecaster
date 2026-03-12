import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
function Forecasts() {
  const [forecasts, setForecasts] = useState([]);
  const [noForecasts, setNoForecasts] = useState(false);
  const API_URL = import.meta.env.VITE_API_URL;
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

  return (
    <>
    {/* Initialises the navifation bar where sellers can move between pages */}
      <nav>
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/current-bundles" className="button"><b>Current Bundles</b></Link>
        <Link to="/add-bundles" className="button"><b>Add Bundles</b></Link>
        <Link to="/analytics" className="button"><b>Analytics</b></Link>
      </nav>

      {/* Forecast data section outputting predictions and IDs */}
      <section>
        {/* Display message while loading forecasts before outputting data*/}
        {forecasts.length === 0 ? (
          <p>Loading forecasts...</p>
        ) : (
          forecasts.map(forecast => (
            <div key={forecast.forecast_id}>              <p>Predicted Reservations: {forecast.predicted_reservations}</p>
              <p>Predicted No-show Probability: {forecast.predicted_no_show_prob}</p>
              <p>User ID : {forecast.user_id}</p>
              <p>Posting ID {forecast.posting_id}</p>
              <p></p>
              <hr />
            </div>
          ))
        )}
        {noForecasts && (
          <p style={{color:"red"}}>
                      No bundles
                  </p>)}
      </section>      
    </>
  );
}
//exports the component so it can be imported in other files
export default Forecasts;

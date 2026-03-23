import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import './Forecast.css'
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
      <div className="forecast">
      {/* Initialises the navifation bar where sellers can move between pages */}
        <div className="pageHeading">
          <nav className="navRow">
            <Link to="/current-bundles" className="button"><b>Current Bundles</b></Link>
            <Link to="/add-bundles" className="button"><b>Add Bundles</b></Link>
            <Link to="/analytics" className="button"><b>Analytics</b></Link>
          </nav>
          <div className="textHeading">
            {/* Header to display the page name to the user */}
            <h1>Forecast</h1>
          </div>
        </div>
      {/* Forecast data section outputting predictions and IDs */}
      <section>
        {/* Display message while loading forecasts before outputting data*/}
        {forecasts.length === 0 ? (
          <h1></h1>
        ) : (
          forecasts.map(forecast => (
            <div key={forecast.forecast_id}>   
              <div className="mainBox">
                <div className="bundleEntry">
                  <h1>Predicted Forecast</h1>
                  <div className="textBox">
                    <p>Predicted Reservations: {forecast.predicted_reservations}</p>
                    <p>Predicted No-show Probability: {forecast.predicted_no_show_prob}</p>
                    <p>User ID : {forecast.user_id}</p>
                    <p>Posting ID {forecast.posting_id}</p>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
        {noForecasts && (
          <div className="mainBox">
            <div className="errorBox">
              <p style={{color:"red"}}>
                  No forecast
              </p>
            </div>
          </div>
        )}
      </section>  
      </div>  
    </>
  );
}
//exports the component so it can be imported in other files
export default Forecasts;

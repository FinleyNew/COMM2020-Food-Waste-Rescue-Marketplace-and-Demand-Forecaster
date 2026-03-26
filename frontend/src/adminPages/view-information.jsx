import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import './view-information.css'
function View_information() {

  const [data,setData] = useState([]); //variable hold all the data retrieved from the requests, needs to be stored in an array, as
  //multiple sets of objects are retrieved


  const handleButtonClick = (value) => {
    let suffix = "";
    switch (value) { //switch statement to get the choice and then build a suffix to use on the request
      case "Get All Consumers":
        suffix="consumers/"; //each suffix is different as it requires a different path to the backend methods
        break;
      case "Get All Sellers":
        suffix="sellers/";
        break;
      case "Get All Bundles":
        suffix="bundles/all";
        break;
      case "Get All Reservations":
        suffix="reservations/";
        break;
      case "Get All Records":
        suffix="records/";
        break;
      case "Get All Forecasts":
        suffix="forecasts/";
        break;
      case "Get All Users":
        suffix="users/";
        break;
      case "Get All Categories":
        suffix="categories/"
        break;
      case "Get All Badges":
        suffix="consumers/badges"
        break;
      case "Get All Issue Reports":
        suffix="reports/"
        break;
      default:
        console.log("Unknown button clicked!");
    }
    const token = localStorage.getItem('token'); //get the token assigned on login to verify a user
    const API_URL = import.meta.env.VITE_API_URL; //get the API URL, which is different depending on if the site is accessed locally or deployed
    console.log(token);
    console.log(`${API_URL}/api/v1/${suffix}`);
    axios.get(`${API_URL}/api/v1/${suffix}`, { //Fetch data for the user
      headers: {
        "Authorization": `Bearer ${token}`, //only need the token to send, not a content type
      }
    })
      .then(response => {
        
        
          setData(response.data); //setting the data to the variable
        
      })
      .catch(err => {
           console.log("status:", err.response?.status); //error catching
           console.log("backend error:", err.response?.data);
      });
  }



  //button values holds all the options an admin can pick to view the data
  const buttonValues = ["Get All Consumers", "Get All Sellers", "Get All Bundles", "Get All Reservations", "Get All Records", "Get All Forecasts", "Get All Users", "Get All Categories", "Get All Badges", "Get All Issue Reports"];
  return (
    <>
    <div className="view">
      {/* Initialises the navifation bar where sellers can move between pages */}
        <nav className="navRow">
          <Link to="/change-information" className="button">Change Information</Link>
          <Link to="/view-tests" className="button">View Tests</Link> {/* navigation buttons to link to the other admin pages */}
        </nav>
        <div className="container">
          <div className="box" style={{ padding: "20px", textAlign: "center" }}>
          <h1 className="header">All Information</h1>
          <div style={{ display: "flex", justifyContent: "center", gap: "10px", flexWrap: "wrap" }}> {/* styling */}
            {buttonValues.map((value, index) => (
              <button className="button"
                key={index}
                onClick={() => handleButtonClick(value)}
                style={{
                  padding: "10px 20px",
                  fontSize: "16px",
                  cursor: "pointer",  //displaying all the choices to view the information
                }}
              >
                {value}
              </button>
            ))}
          </div>
        </div>
      </div>
      <br></br>


      <div className="container">
        <div className="outputBox">
          <h2>Output:</h2>
          {data ? (
            // If data is an array, display as list; otherwise stringify it
            Array.isArray(data) ? (
              <ul>
                {data.map((item, idx) => (
                  <li key={idx}>{JSON.stringify(item)}</li> //dispalying all the data gathered using a map, differs on the number of returned variables
                ))}
              </ul>
            ) : (
              <pre>{JSON.stringify(data, null, 2)}</pre>
            )
          ) : (
            <p>No data fetched yet.</p> //display message if no data is gathered
          )}
        </div>
      </div>
    </div>
    </>
  );
}
//exports the component so it can be imported in other files
export default View_information
import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
function View_information() {

  const [data,setData] = useState([]);


  const handleButtonClick = (value) => {
    let suffix = "";
    switch (value) {
      case "Get All Consumers":
        suffix="consumers/";
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
      default:
        console.log("Unknown button clicked!");
    }
    const token = localStorage.getItem('token');
    const API_URL = import.meta.env.VITE_API_URL;
    console.log(token);
    console.log(`${API_URL}/api/v1/${suffix}`);
    axios.get(`${API_URL}/api/v1/${suffix}`, { //Fetch data for the user
      headers: {
        "Authorization": `Bearer ${token}`,
      }
    })
      .then(response => {
        //setForecasts(response.data); // data is likely an array
        //setAnalytics(response.data);
        console.log("hello");
          setData(response.data)
        
      })
      .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching forecasts:", err);
        alert("No data");
      });
  }



  
  const buttonValues = ["Get All Consumers", "Get All Sellers", "Get All Bundles", "Get All Reservations", "Get All Records", "Get All Forecasts", "Get All Users"];
  return (
    <>
    {/* Initialises the navifation bar where sellers can move between pages */}
      <nav>
        <Link to="/login">Login Page</Link> |{" "}
        <Link to="/change-information">Change Information</Link> |{" "}
        <Link to="/deployment-history">Deployment History</Link>
      </nav>
      <div style={{ padding: "20px", textAlign: "center" }}>
      <h1>All Information</h1>
      <div style={{ display: "flex", justifyContent: "center", gap: "10px", flexWrap: "wrap" }}>
        {buttonValues.map((value, index) => (
          <button
            key={index}
            onClick={() => handleButtonClick(value)}
            style={{
              padding: "10px 20px",
              fontSize: "16px",
              cursor: "pointer",
            }}
          >
            {value}
          </button>
        ))}
      </div>
    </div>


    <div>
      <div>
        <h2>Output:</h2>
        {data ? (
          // If data is an array, display as list; otherwise stringify it
          Array.isArray(data) ? (
            <ul>
              {data.map((item, idx) => (
                <li key={idx}>{JSON.stringify(item)}</li>
              ))}
            </ul>
          ) : (
            <pre>{JSON.stringify(data, null, 2)}</pre>
          )
        ) : (
          <p>No data fetched yet.</p>
        )}
      </div>
    </div>
    </>
  );
}
//exports the component so it can be imported in other files
export default View_information
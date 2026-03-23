import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import Company from "../assets/Company.png";
import './Analytics.css'

function Analytics() {
  const API_URL = import.meta.env.VITE_API_URL;
  const [analytics, setAnalytics] = useState([])
  const [noAnalytics, setNoAnalytics] = useState(false);
  const [logo, setLogo] = useState("");

  
  useEffect(() => {
    const token = localStorage.getItem('token');
    axios.get(`${API_URL}/api/v1/sellers/me`,{
      headers:{
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
    .then(response => {
      
      setLogo(response.data.logo_url);
      console.log(logo);
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching bundles:", err);
        
      });

  },[])


  useEffect(() => {
    const token = localStorage.getItem('token');
    axios.get(`${API_URL}/api/v1/records/me`,{
      headers:{
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
    .then(response => {
      
      if (response.data.length === 0) {
          setNoAnalytics(true);
        } else {
          setAnalytics(response.data);
          setNoAnalytics(false);
        }
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching bundles:", err);
        alert("No data ");
      });

  },[])



  //Calculated totals from arrays retrieved from the backend
  const totalReservations = analytics.reduce(
    (sum,item) => sum + item.observed_reservations,
    0
  );

  const totalNoShows = analytics.reduce(
    (sum, item) => sum + item.observed_no_show,
    0
  );
  const totalWeight = analytics.reduce(
    (sum,item) => sum + item.weight,
    0
  );
  const totalExpired = analytics.reduce(
    (sum,item) => sum + item.observed_expired,
    0
  );

  //Structure for the bar chart displau
  const chartData = [
    { label: "Collected", value: totalReservations, color: "#4CAF50" },
    { label: "No Shows", value: totalNoShows, color: "#fc3d03" },
    { label : "Expired", value: totalExpired, color: "#6f00ff"}
  ];
  //Maximum scaling the bar chart could use
  const maxValue = Math.max(totalReservations,totalNoShows, totalExpired);



  return (
    <>
      <div className="analytics">
        {/* Initialises the navifation bar where sellers can move between pages */}
        <div className="pageHeading">
          <nav class="navRow">
            <Link to="/current-bundles" className="button"><b>Current Bundles</b></Link>
            <Link to="/add-bundles" className="button"><b>Add Bundles</b></Link>
            <Link to="/forecasts" className="button"><b>Forecasts</b></Link>
          </nav>
          
        </div>
          <div className="mainBox">
            <div className="analyticsContent">
              {/* Makes a grid structure with top row containing the company image and circle object with waste prevention stats */}
              <div className="gridRow">
                {/*idx = index */}
                  <div className="barChart">
                    {chartData.map((item, idx) => (  
                      <div key={idx} className="barContainer">
                      <div className="barLabel">{item.label}</div>
                      <div
                        className="bar"
                        style={{
                          height: `${(item.value / maxValue) * 350}px`, // scale bar height
                          backgroundColor: item.color
                        }}
                      >
                    <span className="barValue">{item.value}</span>
                  </div>
                  </div>
                    ))}
                  </div>
                <div className="gridColumn">
                  <p className="bubbleText">Total Waste Prevented</p>
                  <div className="circleObject">
                    <img className="circleBubble" 
                      src="https://img.freepik.com/premium-vector/big-green-sun-vector-icon-green-sun-symbol_302321-2439.jpg?semt=ais_user_personalization&w=740&q=80"></img>
                    <p className="weight">{totalWeight}kg</p>
                  </div>
                </div>
                <img className="companyImage" src={logo}></img>
              </div>
            </div>
            <div className="textHeading">
              <h2>Data</h2>
            </div>
            <div className="analyticsContent">
              <div className="gridRow">
                {/* Desciption entries outputted to screen with the user_id */}
                {analytics.map(analytic => (
                    <div key={analytic.posting_id}>
                      <div className="desc">
                      <p className="desc">user_id - {analytic.user_id}</p>
                        <p className="desc">Company - Amazon</p>
                        <p className="desc">Price - {analytic.price}</p>
                        <p className="desc">Category - {analytic.category.name}</p>
                        <p className="desc">Reservations - {analytic.observed_reservations}</p>
                        <p className="desc">No Shows - {analytic.observed_no_show}</p>
                        <p className="desc">Expired - {analytic.observed_expired}</p>
                        <p className="desc">Pickup Date - {analytic.pickup_date}</p>
                        <p className="desc">Pickup Date Formatted - {analytic.formatted_date}</p>
                        <p className="desc">Raining - {analytic.raining.toString()}</p>
                        <p className="desc">Weight - {analytic.weight}</p>
                        
                      </div>
                    </div>
                  ))
                }
              </div>
          </div>
          </div>
        </div>
        {noAnalytics && (
            <p style={{color:"red"}}>
                        No Analytics
                    </p>)}
    </>
  );
}
//exports the component so it can be imported in other files
export default Analytics
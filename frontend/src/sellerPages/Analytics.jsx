import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";



import './Analytics.css'

function Analytics() {
  const [analytics, setAnalytics] = useState([])
  useEffect(() => {
    const token = localStorage.getItem('token');
    fetch("http://127.0.0.1:8000/api/v1/records/me",{
      headers:{
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    }) //fetch here , useeffect means it only fetches once
      .then(res => res.json())
      .then(data => {
        console.log("API DATA:", data); 
        setAnalytics(data);
      })
      .catch(err => {
        console.error("Error fetching bundles:", err);
        alert("No data ");
      });
  }, []);
  const totalReservations = analytics.reduce(
    (sum,item) => sum + item.observed_reservations,
    0
  );

  const totalNoShows = analytics.reduce(
    (sum, item) => sum + item.observed_no_show,
    0
  );

  const chartData = [
    { label: "Reservations", value: totalReservations, color: "#4CAF50" },
    { label: "No Shows", value: totalNoShows, color: "#FF5722" }
  ];

  const maxValue = Math.max(totalReservations,totalNoShows);



  return (
    <>
      <nav class="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/current-bundles" className="button"><b>Current Bundles</b></Link>
        <Link to="/add-bundles" className="button"><b>Add Bundles</b></Link>
        <Link to="/forecasts" className="button"><b>Forecasts</b></Link>
      </nav>
      
      <section>
        {analytics.map(analytic => (
            <div key={analytic.posting_id}>
              <div className="desc">
               <p className="desc">user_id - {analytic.user_id}</p>
                <p className="desc">Company - Amazon</p>
                <p className="desc">Price - {analytic.price}</p>
                <p className="desc">Category - {analytic.category}</p>
                <p className="desc">Reservations - {analytic.observed_reservations}</p>
                <p className="desc">No Shows - {analytic.observed_no_show}</p>
                <p className="desc">Pickup Date - {analytic.pickup_date}</p>
                <p className="desc">Pickup Date Formatted - {analytic.formatted_date}</p>
                <p className="desc">Raining - {analytic.raining.toString()}</p>
              </div>
            </div>
          ))
        }
      </section>
      {/*idx = index */}
      <div className="barChart">
        {chartData.map((item, idx) => (  
          <div key={idx} className="barContainer">
          <div className="barLabel">{item.label}</div>
          <div
            className="bar"
            style={{
              height: `${(item.value / maxValue) * 200}px`, // scale bar height
              backgroundColor: item.color
            }}
          >
        <span className="barValue">{item.value}</span>
      </div>
      </div>
        ))}
      </div>

      <div className="gridRow">
        <img className="companyImage" src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M="></img>
        <div className="gridColumn">
          <p className="bubbleText">Total Waste Prevented</p>
          <div className="circleObject">
            <img className="circleBubble" 
              src="https://img.freepik.com/premium-vector/big-green-sun-vector-icon-green-sun-symbol_302321-2439.jpg?semt=ais_user_personalization&w=740&q=80"></img>
            <p className="weight">52kg</p>
          </div>
        </div>
      </div>
        <div className="gridRow">
          <img className="imageFormatter" src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M="></img>
              <div className="gridColumn">
                <img src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M="></img>
              </div>
      </div>
    </>
  );
}

export default Analytics
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
                <p className="desc">Raining - {analytic.raining.toString()}</p>
              </div>
            </div>
          ))
        }
      </section>
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
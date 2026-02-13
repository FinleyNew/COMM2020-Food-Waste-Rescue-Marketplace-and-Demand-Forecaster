import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import './Discover.css'
function Codes() {
  const [bundles, setBundles] = useState([]); //create state
    
    useEffect(() => {
      const token = localStorage.getItem('token');
      fetch("http://127.0.0.1:8000/api/v1/reservations/me",{
        headers:{
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      }) //fetch here , useeffect means it only fetches once
        .then(res => res.json())
        .then(data => {
          console.log("API DATA:", data); 
          setBundles(data);
        })
        .catch(err => {
          console.error("Error fetching bundles:", err);
          alert("No data ");
        });
    }, []);
    if (!bundles) return <p>Loading bundle...</p>;
  
  return (
      <>
        <nav class="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/discover" className="button"><b>Discover</b></Link>
        <Link to="/streaks" className="button"><b>Streaks</b></Link>
      </nav>
      <h1 className="headline">Codes</h1>
      <section className="column">
        {bundles.map(bundle => (
          <div key={bundle.posting_id}>
              <section>
          <div className="textBlock">
            <img src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M=" alt="Food" className="leftImg"/>
            <div className="desc">
              <p className="desc">Reservation ID : {bundle.reservation_id}</p>
              <p className="desc">Claim Code - {bundle.claim_code}</p>
            </div>
          </div>
          <div className="textBlock">
            <div className="desc">
              <p className="codeText">Status - {bundle.status}</p>
              
              <p>Collection Time - {bundle.timestamp}</p>
            </div>
          </div>
          </section>
          </div>
        ))}



      </section>
      
      </>
    );
}

export default Codes

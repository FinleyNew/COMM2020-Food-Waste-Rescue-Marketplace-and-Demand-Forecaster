import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";

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

    </>
  );
}

export default Analytics
import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";

function Analytics() {
  const [analytics, setAnalytics] = useState(null)
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
  if (!analytics) return <p>Loading analytics...</p>;

  return (
    <>
      <nav class="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/current-bundles" className="button"><b>Current Bundles</b></Link>
        <Link to="/add-bundles" className="button"><b>Add Bundles</b></Link>
      </nav>
      <section>
        {analytics && (
          <div className="desc">
            <p className="desc">user_id - {analytics.user_id}</p>
            <p className="desc">Company - Amazon</p>
            <p className="desc">Price - {analytics.price}</p>
            <p className="desc">Category - {analytics.category}</p>
            <p className="desc">Raining - {analytics.raining.toString()}</p>
          </div>
        )}
      </section>

    </>
  );
}

export default Analytics
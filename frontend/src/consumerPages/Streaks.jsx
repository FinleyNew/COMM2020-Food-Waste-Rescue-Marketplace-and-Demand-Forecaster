import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import './Discover.css'
function Streaks() {
  const [bundle,setBundle] = useState(null);
  useEffect(() => {
  const token = localStorage.getItem('token');

  fetch("http://127.0.0.1:8000/api/v1/consumers/me", {
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    }
  })
    .then(res => res.json())
    .then(data => {
      setBundle(data);
    })
    .catch(err => {
      console.error("Error fetching bundles:", err);
      alert("No data");
    });

}, []);


  return (
      <>
        <nav class="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/discover" className="button"><b>Discover</b></Link>
        <Link to="/codes" className="button"><b>Codes</b></Link>
      </nav>
      <h1 className="headline">Streaks</h1>
      <p className="textCentre">You have rescued for  weeks in a row!</p><hr></hr>
      <div className="rowIcons">
        <p className="headline">Badges:</p>
        <img className="icon" src="https://thumbs.dreamstime.com/b/modern-bronze-circle-metal-badges-labels-design-elements-vector-illustration-84952346.jpg" alt="Bronze Badge"/>   
        <img className="icon" src="https://img.favpng.com/11/16/23/gold-medal-silver-medal-illustration-png-favpng-vJK1hRCuK1bUdtG0Hb4dJ7VkU.jpg" alt="Silver Badge"/>   
        <img className="icon" src="https://www.onlygfx.com/wp-content/uploads/2022/04/blank-gold-badge-label-2.png" alt="Gold Badge"/>   
      </div>
      <hr></hr>
      <p>Summary PIS</p>

      {bundle && (
        <div>
          <h1>streak: {bundle.streak}</h1>
          <h1>userID: {bundle.user_id}</h1>
        </div>
      )}


      </>
    );
}

export default Streaks;

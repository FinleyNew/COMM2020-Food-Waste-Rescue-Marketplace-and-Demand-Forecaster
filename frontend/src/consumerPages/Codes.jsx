import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import './Codes.css'
import Company from "../assets/BundleImage.png";
import axios from "axios";
function Codes() {
  const API_URL = import.meta.env.VITE_API_URL;
  const [bundles, setBundles] = useState([]); //needs an empty array as it will display a list of data instead of of one object
  const [noBundles, setNoBundles] = useState(false);
    


    useEffect(() => { //use effect allows the command run on entering the page and if anything changes
      const token = localStorage.getItem('token'); //defines the token which we need to authorize the user and get their data
      axios.get(`${API_URL}/api/v1/reservations/me`,{ //the server url to get the information for 
        headers: {
          "Authorization": `Bearer ${token}`, //sending the token to verify the user
          "Content-Type": "application/json" //defines that we are getting a JSON object/piece of data
        }
      })
      .then(response => {
        if (response.data.length === 0) {
          setNoBundles(true);
        } else {
          setBundles(response.data);
          setNoBundles(false);
  }
})
      .catch(err =>{
        console.error("request failed",err);
      })
    },[]) //if anything changes reload the page




    if (!bundles) return <p>Loading bundle...</p>;
  
  return (
      <>
      <div className="codes">
        <div className="pageHeading">
          <nav className="navRow">
            <Link to="/discover" className="button"><b>Discover</b></Link> {/* defines the links to the other other pages */}
            <Link to="/streaks" className="button"><b>Streaks</b></Link>
          </nav>
          <nav class="textHeading">
              <h1>Codes</h1>
          </nav>
        </div>
        {bundles.map((bundle) => (
    <div className="mainBox">
      <div className="bundleEntry">
        <div className="textBox">
          <div className="bundleRow">
            <h1>{bundle.posting.seller.name}</h1>
            <h2>Claim Code: {bundle.claim_code}</h2>
          </div>

          <div className="bundleRow">
            <div className="column">
              <p>
                Status:{" "}
                <span className={`status${bundle.status.toLowerCase()}`}>
                  {bundle.status.toUpperCase()}
                </span>
              </p>
              <p>Pickup Date: {bundle.posting.formatted_date}</p>
              <p>Pickup Time: {bundle.posting.formatted_time_range}</p>
            </div>

            <div className="column">
              <img
                src={bundle.posting.seller.logo_url}
                alt="Company"
                className="companyIcon"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  
))}
        {noBundles && (
        <div className="mainBox">  
          <p className="errorBox" style={{color:"red"}}>
                      No bundles
                  </p></div>)}
      </div>
      </>
    );
}

export default Codes; //exports the component so it can be imported in other files

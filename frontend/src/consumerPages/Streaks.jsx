import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import './Streaks.css'
import noBadge from "../assets/NoBadge.png";
import Badge from "../assets/Badge.png";
import axios from "axios";
function Streaks() {
  const API_URL = import.meta.env.VITE_API_URL;
  const [bundle,setBundle] = useState(""); //defines the state and variable that allows the react page to be rerendered when called, no array as its one object that's returned
  const [badges, setBadges] = useState([]);
  const [allBadges, setAllBadges] = useState([]);
  const [impactSummary, setImpactSummary] = useState("");

  useEffect(() => { //useEffect allows the command run on entering the page and if anything changes
    const token = localStorage.getItem('token'); //defines the token which we need to authorize the user and get their data
    axios.get(`${API_URL}/api/v1/consumers/me`,{ //the backend server url to get the information for 
      headers: {
        "Authorization": `Bearer ${token}`, //sending the token to verify the user
        "Content-Type": "application/json" //defines that we are getting a JSON object/piece of data
      }
    })
    .then(response => {
      setBundle(response.data); //updates the react state so the page can rerender with the new info
    })
    .catch(err => {
          console.error("Error fetching bundles:", err); //catches any errors and displays an erorr messages 
          alert("No data ");
    });
  },[]) //allows the page to rerender if anything changes

  useEffect(() => { //useEffect allows the command run on entering the page and if anything changes
    const token = localStorage.getItem('token'); //defines the token which we need to authorize the user and get their data
    axios.get(`${API_URL}/api/v1/consumers/me/badges`,{ //the backend server url to get the information for 
      headers: {
        "Authorization": `Bearer ${token}`, //sending the token to verify the user
      }
    })
    .then(response => {
      setBadges(response.data); //updates the react state so the page can rerender with the new info
      
    })
    .catch(err => {
          console.error("Error fetching badges:", err); //catches any errors and displays an erorr messages 
          alert("No data ");
    });
    
  },[]) //allows the page to rerender if anything changes

  useEffect(() => {
      const token = localStorage.getItem('token');
     axios.get(`${API_URL}/api/v1/consumers/me/personal-impact-summary`,{ //the backend server url to get the information for 
      headers: {
        "Authorization": `Bearer ${token}`, //sending the token to verify the user
      }
    })
    .then(response => {
      setImpactSummary(response.data);
    })
  }, [])


  useEffect(() => {
     axios.get(`${API_URL}/api/v1/consumers/badges`,{ //the backend server url to get the information for 
      
    })
    .then(response => {
      setAllBadges(response.data);
    })
  }, [])

  

  return (
      <>
        <div className="streaks">
          <div className="pageHeading">
            <nav className="navRow">
              <Link to="/discover" className="button"><b>Discover</b></Link> {/* displays the links to the other pages */}
              <Link to="/codes" className="button"><b>Codes</b></Link>
            </nav>
            <div className="textHeading">
              <h1>Streaks</h1>
            </div>
          </div>
          <div className="mainBox">
            <div className="streaksEntry">
              {bundle && (
                <div>
                  <p className="textCentre">{bundle.display_name} has rescued for {bundle.streak} week(s) in a row!</p><hr></hr> {/* message to display the streak */}
                </div>
              )}
              <div className="textBox">
                <h3>Personal Impact Summmary</h3> {/* summary statement */}
                <p>
                  {bundle.display_name} has made {impactSummary.total_reservations_made} reservations, collecting {impactSummary.total_collected} and not showing for {impactSummary.total_no_shows}, giving them a collection success rate of {impactSummary.collection_success_rate}%.
                </p>

              <p>
                In total, they saved {impactSummary.waste_saved_kg}kg worth of food! Whilst saving an estimated {impactSummary.co2_estimate_saved}kg of CO2.
              </p>

              <p>
                They have made {impactSummary.collections_this_month} collections this month with a favourite category of {impactSummary.favourite_category} and have achieved a streak of {impactSummary.streak}, whilst earning {impactSummary.badges_earned} badges!
              </p>
                
              </div>
              <p className="textCentre">Badges</p>
              <div className="rowIcons">
                {allBadges.slice(0,4).map((badge)=> {
                  const unlock = badges.some(userBadge => userBadge.name === badge.name);
                  return (
                    <div key={badge.badge_id} className="badges">
                      <img className="icon" src={unlock ? Badge : noBadge}></img>
                      <div className="hoverDesc">
                        {badge.name}
                        <br></br>
                        {unlock ? badge.detail : "Badge is Locked"}
                      </div>
                    </div>
                  );
                })}
              </div>
              <div className="rowIcons">
                {allBadges.slice(4,8).map((badge)=> {
                  const unlock = badges.some(userBadge => userBadge.name === badge.name);
                  return (
                    <div key={badge.badge_id} className="badges">
                      <img className="icon" src={unlock ? Badge : noBadge}></img>
                      <div className="hoverDesc">
                        {badge.name}
                        <br></br>
                        {unlock ? badge.detail : "Badge is Locked"}
                      </div>
                    </div>
                  );
                })}
              </div>
              <div className="rowIcons">
                {allBadges.slice(8,12).map((badge)=> {
                  const unlock = badges.some(userBadge => userBadge.name === badge.name);
                  return (
                    <div key={badge.badge_id} className="badges">
                      <img className="icon" src={unlock ? Badge : noBadge}></img>
                      <div className="hoverDesc">
                        {badge.name}
                        <br></br>
                        {unlock ? badge.detail : "Badge is Locked"}
                      </div>
                    </div>
                  );
                })}
              </div>
              <div className="rowIcons">
                {allBadges.slice(12,16).map((badge)=> {
                  const unlock = badges.some(userBadge => userBadge.name === badge.name);
                  return (
                    <div key={badge.badge_id} className="badges">
                      <img className="icon" src={unlock ? Badge : noBadge}></img>
                      <div className="hoverDesc">
                        {badge.name}
                        <br></br>
                        {unlock ? badge.detail : "Badge is Locked"}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      </>
    );
}

export default Streaks; //exports the component so it can be imported in other files
import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import './Streaks.css'
import noBadge from "../assets/NoBadge.png";
import axios from "axios";
function Streaks() {
  const API_URL = import.meta.env.VITE_API_URL;
  const [bundle,setBundle] = useState(null); //defines the state and variable that allows the react page to be rerendered when called, no array as its one object that's returned
  const [badges, setBadges] = useState([]);

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
    
  },[badges]) //allows the page to rerender if anything changes

  

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
                <p>Summary PIS</p> {/* summary statement */}
              </div>
              <p className="textCentre">Badges</p>
              <div className="rowIcons">
                <div className="badges">
                  <div className="icon" src={noBadge}></div>
                  <div className="hoverDesc">
                    Badge is Locked
                  </div>
                </div>
                <div className="badges">
                  <div className="icon" src={noBadge}></div>
                  <div className="hoverDesc">
                    Badge is Locked
                  </div>
                </div>
                <div className="badges">
                  <div className="icon" src={noBadge}></div>
                  <div className="hoverDesc">
                    Badge is Locked
                  </div>
                </div>
                <div className="badges">
                  <div className="icon" src={noBadge}></div>
                  <div className="hoverDesc">
                    Badge is Locked
                  </div>
                </div>
              </div>
              <div className="rowIcons">
                <div className="badges">
                  <div className="icon" src={noBadge}></div>
                  <div className="hoverDesc">
                    Badge is Locked
                  </div>
                </div>
                <div className="badges">
                  <div className="icon" src={noBadge}></div>
                  <div className="hoverDesc">
                    Badge is Locked
                  </div>
                </div>
                <div className="badges">
                  <div className="icon" src={noBadge}></div>
                  <div className="hoverDesc">
                    Badge is Locked
                  </div>
                </div>
                <div className="badges">
                  <div className="icon" src={noBadge}></div>
                  <div className="hoverDesc">
                    Badge is Locked
                  </div>
                </div>
              </div>
              <div className="rowIcons">
                <div className="badges">
                  <div className="icon" src={noBadge}></div>
                  <div className="hoverDesc">
                    Badge is Locked
                  </div>
                </div>
                <div className="badges">
                  <div className="icon" src={noBadge}></div>
                  <div className="hoverDesc">
                    Badge is Locked
                  </div>
                </div>
                <div className="badges">
                  <div className="icon" src={noBadge}></div>
                  <div className="hoverDesc">
                    Badge is Locked
                  </div>
                </div>
                <div className="badges">
                  <div className="icon" src={noBadge}></div>
                  <div className="hoverDesc">
                    Badge is Locked
                  </div>
                </div>
              </div>
              <div className="rowIcons">
                <div className="badges">
                  <div className="icon" src={noBadge}></div>
                  <div className="hoverDesc">
                    Badge is Locked
                  </div>
                </div>
                <div className="badges">
                  <div className="icon" src={noBadge}></div>
                  <div className="hoverDesc">
                    Badge is Locked
                  </div>
                </div>
                <div className="badges">
                  <div className="icon" src={noBadge}></div>
                  <div className="hoverDesc">
                    Badge is Locked
                  </div>
                </div>
                <div className="badges">
                  <div className="icon" src={noBadge}></div>
                  <div className="hoverDesc">
                    Badge is Locked
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>



        <div>
  {badges.map((badge, idx) => (
    <div key={idx} className="badge">
      <h3>{badge.name}</h3>
      <p>{badge.detail}</p>
    </div>
  ))}
</div>
      </>
    );
}

export default Streaks; //exports the component so it can be imported in other files

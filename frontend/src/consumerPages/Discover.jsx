import { Routes, Route, Link } from "react-router-dom";
import {useState, useEffect} from "react";
import './Discover.css'

import Company from "../Assets/Company.png";
import Bundle from "../Assets/Bundleimage.png";
function Discover() {
  
  const [bundles, setBundles] = useState([]); //defines the state and variable that allows the react page to be rerendered when called

  useEffect(() => { //useEffect allows the command run on entering the page and if anything changes
      const token = localStorage.getItem('token'); //defines the token which we need to authorize the user and get their data
      fetch("http://127.0.0.1:8000/api/v1/bundles/",{ //the backend server url to get the information for 
        headers:{
          "Content-Type": "application/json" //defines that we are getting a JSON object/piece of data
        }
      }) //fetch here , useeffect means it only fetches once
        .then(res => res.json()) //converts the data into an object JSON
        .then(data => {
          console.log("API DATA:", data); 
          setBundles(data); //updates the react state so the page can rerender with the new info
        })
        .catch(err => {
          console.error("Error fetching bundles:", err); //catches any errors and displays an erorr messages 
          alert("No data ");
        });
    }, []);
  return (
    <>
      <nav class="row">
        <Link to="/login" className="button"><b>Login Page</b></Link> {/* displays the links to the other pages */}
        <Link to="/streaks" className="button"><b>Streaks</b></Link>
        <Link to="/codes" className="button"><b>Codes</b></Link>
        <details>
          <summary>
            <img className="setting" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBdndCKhAJ4SlVEaNCkA4U6BN4tDXZsRtxSw&s"></img> {/* holds the images for the settings page */}
          </summary>
          <label>
            <input type="checkbox" name="darkmode"/> {/* checkbox for darkmode */}
              Enable Dark Mode DOESNT WORK YET
          </label>
        </details>
      </nav>
      <h1 className="headline">Bundles</h1>
      
      <section className="column">
            {bundles.map(bundle => ( //have to use a map as there are multiple objects all with multiple data attributes, so using a map to traverse them
              <div key={bundle.posting_id}> {/* needs a key to uniquely identify a specific object when traversing through them all */}
                <Link to={`/bundle/${bundle.posting_id}`} className="sectionPage">

                  <section className="bundleEntry">
                    <div className="textBlock">
                      <img src={Company} alt="Company" className="leftImg"/>
                      <div className="desc">
                        <p className="desc">Category - {bundle.category}</p>
                        <p className="desc">Allergens - {bundle.allergens}</p>
                      </div>
                    </div>
                    <div className="textBlock">
                      <div className="desc">
                      <p className="desc">Available - {bundle.available}</p>
                      <p className="desc">Price - £{bundle.price_display}</p> {/* displaying all the information by accessing the specific object */}
                      <p className="desc">Date to Collect - {bundle.formatted_date}</p>
                      <p className="desc">Time to Collect - {bundle.formatted_time_range}</p>
                       </div>
                    </div>
                    <div className="formatter">
                      <img src={Bundle} alt="Food" className="thumbnail"/>
                      {/*<p className="desc">{companyName}</p>*/}
                    </div>
                  </section>
                </Link>
                <div className="whitespace" aria-hidden="true"></div>
              </div>
            ))}
      </section>
    </>
  );
}

export default Discover; //exports the component so it can be imported in other files

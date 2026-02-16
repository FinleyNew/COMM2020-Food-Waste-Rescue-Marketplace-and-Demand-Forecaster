import { Routes, Route, Link } from "react-router-dom";
import {useState, useEffect} from "react";
import './Discover.css'
import Company from "../Assets/Company.png";
import Bundle from "../Assets/Bundleimage.png";
function Discover() {
  let companyName = "Amazon";
  let category = "Fruit";
  let bundleName = "idk";
  let location = "EX1 2HR";
  let collectionTime = "12:00";
  const [bundles, setBundles] = useState([]);

  useEffect(() => {
      const token = localStorage.getItem('token');
      fetch("http://127.0.0.1:8000/api/v1/bundles/",{
        headers:{
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
  return (
    <>
      <nav class="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/streaks" className="button"><b>Streaks</b></Link>
        <Link to="/codes" className="button"><b>Codes</b></Link>
        <details>
          <summary>
            <img className="setting" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBdndCKhAJ4SlVEaNCkA4U6BN4tDXZsRtxSw&s"></img>
          </summary>
          <label>
            <input type="checkbox" name="darkmode"/>
              Enable Dark Mode DOESNT WORK YET
          </label>
        </details>
      </nav>
      <h1 className="headline">Bundles</h1>
      
      <section className="column">
            {bundles.map(bundle => (
              <div key={bundle.posting_id}>
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
                      <p className="desc">Availbale - {bundle.available}</p>
                      <p className="desc">Price - {bundle.price_display}</p>
                      <p className="desc">Collection Time - {bundle.end_time}</p>
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

export default Discover

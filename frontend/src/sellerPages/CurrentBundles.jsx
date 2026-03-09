import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import './CurrentBundles.css'
import Company from "../assets/Company.png";
import Bundle from "../assets/BundleImage.png";
import axios from "axios";
function CurrentBundles() {
  const API_URL = import.meta.env.VITE_API_URL;
  const [bundles, setBundles] = useState([]); //create state
  const [code, setCode] = useState("");

  const navigate = useNavigate();
  


  useEffect(() => {
    const token = localStorage.getItem('token');
    axios.get(`${API_URL}/api/v1/bundles/me`, {
      headers:{
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
    .then(response => {
      setBundles(response.data);
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching bundles:", err);
        alert("No data ");
      });
  },[])



  const deleteBundle = (posting_id) => { //Function to delete bundles from backend
    const API_URL = import.meta.env.VITE_API_URL;
    if (!window.confirm("Delete this bundle?")) return;

    axios.get(`${API_URL}/api/v1/bundles/${posting_id}`, {
    
    })
    .then(response => {
      console.log("Deleted:", response.data);
      alert("Bundle deleted");
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching bundles:", err);
        alert("No data ");
    });
    
    
};

const enterCode = (claim_code) => { //Function to return an entered code from the backend
  if (!window.confirm("Collect this bundle?")) return;
  const API_URL = import.meta.env.VITE_API_URL;
  const token = localStorage.getItem('token'); 

  axios.get(`${API_URL}/api/v1/reservations/collect/${claim_code}`, { //Fetches inputted tocken
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    }
  })
    .then(response => {
      console.log("Collected:", response.data);
      alert("Bundle collected");
    })
    .catch(err => console.error(err));
};


  return (
    <>
    {/* Initialises the navifation bar where sellers can move between pages */}
      <nav className="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/add-bundles" className="button"><b>Add Bundles</b></Link>
        <Link to="/analytics" className="button"><b>Analytics</b></Link>
        <Link to="/forecasts" className="button"><b>Forecasts</b></Link>
      </nav>
      {/* Header to display the page name to the user */}
      <h1 className="headline">Bundles</h1>
      {/* Section for the code input and submission button */}
       <form onSubmit={(e) => {
              e.preventDefault();
              enterCode(code);
            }}>
              <input
                id="enterCode"
                type="text"
                placeholder="enter code"
                value={code}
                onChange={(e) => setCode(e.target.value)}
              />
              <button type="submit">Confirm Collection</button>

            </form>
            <br></br>
      {/* Columns structure for displaying bundle infomation */}
      <section className="column">
        {bundles.map(bundle => ( //.map allows us to display
          <div key={bundle.posting_id}>
            <div className="bundleEntry">
              {/* Contains company image and first column data */}
              <div className="textBlock">
                <img
                  src={Company}
                  alt="Company"
                  className="leftImg"
                />
                <div className="desc">
                  <p className="desc">Price - £{bundle.price_display}</p>
                  <p className="desc">Category - {bundle.category}</p>
                  <p classname="desc">Available - {bundle.available}</p>
                </div>
              </div>
              {/* Holds the middle column data for the bundle entry */}
              <div className="textBlock">
                <div className="desc">
                  <p className="desc">Allergens - {bundle.allergens} </p>
                  <p className="desc">Date to Collect - {bundle.formatted_date}</p>
                  <p className="desc">Time to Collect - {bundle.formatted_time_range}</p>
                  <p className="desc">Weight - {bundle.weight}</p>
                  <p className="desc">Reserved - {bundle.reserved}</p>
                </div>
              </div>
              {/* Final row bundle image */}
              <div className="formatter">
                <img
                  src={Bundle}
                  alt="Bundle"
                  className="thumbnail"
                />
              </div>
              <br></br>
            </div>
            {/* Button to delete bundles on click */}
            <button onClick={() => deleteBundle(bundle.posting_id)}>
                Delete Bundle
              </button>
        </div>
        ))}
      </section>
    </>
  );
}
//exports the component so it can be imported in other files
export default CurrentBundles;
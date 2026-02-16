import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import './CurrentBundles.css'
import Company from "../Assets/Company.png";
import Bundle from "../Assets/Bundleimage.png";
function CurrentBundles() {
  
  const [bundles, setBundles] = useState([]); //create state
  const [code, setCode] = useState("");

  const navigate = useNavigate();
  useEffect(() => {
    const token = localStorage.getItem('token');
    fetch("http://127.0.0.1:8000/api/v1/bundles/me",{
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
  const deleteBundle = (posting_id) => {
    if (!window.confirm("Delete this bundle?")) return;

    fetch(`http://127.0.0.1:8000/api/v1/bundles/${posting_id}`, {
    method: "GET"
    })
    .then(res => res.json())
    .then(data => {
      console.log("Deleted:", data);
      alert("Bundle deleted");
    })
    
    .catch(err => console.error(err));
};

const enterCode = (claim_code) => {
  if (!window.confirm("Collect this bundle?")) return;

  const token = localStorage.getItem('token');

  fetch(`http://127.0.0.1:8000/api/v1/reservations/collect/${claim_code}`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    }
  })
    .then(res => res.json())
    .then(data => {
      console.log("Collected:", data);
      alert("Bundle collected");
    })
    .catch(err => console.error(err));
};


  return (
    <>
      <nav className="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/add-bundles" className="button"><b>Add Bundles</b></Link>
        <Link to="/analytics" className="button"><b>Analytics</b></Link>
        <Link to="/forecasts" className="button"><b>Forecasts</b></Link>
      </nav>

      <h1 className="headline">Bundles</h1>
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
      <section className="column">
        {bundles.map(bundle => ( //.map allows us to display
          <div key={bundle.posting_id}>
            <div className="bundleEntry">
              <div className="textBlock">
                <img
                  src={Company}
                  alt="Company"
                  className="leftImg"
                />
                <div className="desc">
                  <p classname="desc">user_id - {bundle.user_id} </p>
                  
                  <p className="desc">Price - {bundle.price}</p>
                  <p className="desc">Category - {bundle.category}</p>
                  <p classname="desc">Available - {bundle.available}</p>
                </div>
              </div>

              <div className="textBlock">
                <div className="desc">
                  <p className="desc">Allergens - {bundle.allergens} </p>
                  <p className="desc">Location - </p>
                  <p className="desc">Collection Time -{bundle.start_time} </p>
                  <p className="desc">Collection Time2 -{bundle.end_time} </p>
                </div>
              </div>

              <div className="formatter">
                <img
                  src={Bundle}
                  alt="Bundle"
                  className="thumbnail"
                />
                {/* <p className="desc">Company Name - {bundle.companyName}</p> */}
              </div>
              <br></br>
            </div>
            <button onClick={() => deleteBundle(bundle.posting_id)}>
                Delete Bundle
              </button>
              {/*works but need to use docker compose down -v */}
              <div className="whitespace" aria-hidden="true"></div>
        </div>
        ))}
      </section>
    </>
  );
}

export default CurrentBundles;
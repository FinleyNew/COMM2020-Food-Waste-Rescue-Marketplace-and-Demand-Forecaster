import { Routes, Route, Link } from "react-router-dom";
import { useParams } from "react-router-dom";
import {useState, useEffect} from "react";

function BundleSelect() {
  let companyName = "Amazon";
  let category = "Fruit";
  let bundleName = "idk";
  let location = "EX1 2HR";
  let collectionTime = "12:00";
  let allergens = "none";
  const { id } = useParams();
  const [bundle, setBundle] = useState(null);

  useEffect(() => {
  fetch(`http://127.0.0.1:8000/api/v1/bundles/${id}`)
    .then(res => res.json())
    .then(data => {
      console.log("Bundle data:", data);
      setBundle(data);
    })
    .catch(err => console.error(err));
  }, [id]);
  if (!bundle) return <p>Loading bundle...</p>; //needs this as the react loads faster than the fetch, tries to access a data point before it exists
  return (
      <>
      
       <nav className="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/discover" className="button"><b>Discover</b></Link>
        <Link to="/streaks" className="button"><b>Streaks</b></Link>
        <Link to="/codes" className="button"><b>Codes</b></Link>
      </nav>
      <h1 className="headline">Bundles</h1>
      <section>
        <div className="textBlock">
          <img src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M=" alt="Food" className="leftImg"/>
          <div className="desc">
            <p className="desc">Category - {bundle.category}</p>
            <p className="desc">Allergens - {bundle.allergens}</p>
          </div>
        </div>
        <div className="textBlock">
          <div className="desc">
            <p className="desc">Bundle Name - {bundleName}</p>
            <p className="desc">Location - {location}</p>
            <p className="desc">Collection Time - {collectionTime}</p>
            <p className="desc">Allergens - {allergens}</p>
          </div>
        </div>
        <div className="formatter">
          <img src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M=" alt="Food" className="thumbnail"/>
            <p className="desc">Company Name - {companyName}</p>
          </div>
        <div className="formatter">
          <button>+</button>
          <button>-</button>
        </div>
        </section>


        
      </>
    );
}

export default BundleSelect;
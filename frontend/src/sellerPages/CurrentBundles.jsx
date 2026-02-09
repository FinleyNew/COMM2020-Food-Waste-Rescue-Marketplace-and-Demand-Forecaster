
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";

function CurrentBundles() {

  const [bundles, setBundles] = useState([]); //create state

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/bundles/") //fetch here , useeffect means it only fetches once
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
      <nav className="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/add-bundles" className="button"><b>Add Bundles</b></Link>
        <Link to="/analytics" className="button"><b>Analytics</b></Link>
      </nav>

      <h1 className="headline">Bundles</h1>

      <section>
        {bundles.map(bundle => ( //.map allows us to display
          <div key={bundle.posting_id}>

            <div className="textBlock">
              <img
                src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M="
                alt="Food"
                className="leftImg"
              />
              <div className="desc">
                <p className="desc">Company - </p>
                <p className="desc">Category - {bundle.category}</p>
              </div>
            </div>

            <div className="textBlock">
              <div className="desc">
                <p className="desc">Bundle Name - {bundle.allergens} </p>
                <p className="desc">Location - </p>
                <p className="desc">Collection Time - </p>
              </div>
            </div>

            <div className="formatter">
              <img
                src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M="
                alt="Food"
                className="thumbnail"
              />
              <p className="desc">Company Name - {bundle.companyName}</p>
            </div>

            <div className="formatter">
              <p className="button">Edit</p>
              <p className="button">Delete</p>
            </div>

          </div>
        ))}
      </section>
    </>
  );
}

export default CurrentBundles;


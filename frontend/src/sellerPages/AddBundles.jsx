import { Routes, Route, Link } from "react-router-dom";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function AddBundles() {
  const [bundleName, setBundleName] = useState("");
  const [location, setLocation] = useState("");
  const [collectionTime, setCollectionTime] = useState("");

  function addBundle(){
    const data = {
      bundleName: bundleName,
      location: location,
      collectionTime: collectionTime
    };

    fetch("http://localhost:5000/api/add-bundles", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });
  }

  return (
    <>
      <nav className="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/current-bundles" className="button"><b>Current Bundles</b></Link>
        <Link to="/analytics" className="button"><b>Analytics</b></Link>
      </nav>

      <h1 className="headline">Add Bundles</h1>

      <section>
        <div className="textBlock">

          <label htmlFor="bundle_name">Enter Bundle Name :</label>
          <input
            id="bundle_name"
            type="text"
            value={bundleName}
            onChange={(e) => setBundleName(e.target.value)}
          />

          <br />

          <label htmlFor="location">Enter Location :</label>
          <input
            id="location"
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />

          <br />

          <label htmlFor="collectionTime">Enter Collection Time :</label>
          <input
            id="collectionTime"
            type="text"
            value={collectionTime}
            onChange={(e) => setCollectionTime(e.target.value)}
          />

          <button onClick={addBundle}>Add Bundle</button>

        </div>
      </section>
    </>
  );
}

export default AddBundles;

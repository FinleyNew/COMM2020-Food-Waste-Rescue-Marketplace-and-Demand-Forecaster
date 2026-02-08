import { Routes, Route, Link } from "react-router-dom";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function AddBundles() {
  let bundleName = "";
  let location = "";
  let collectionTime = "";
  function addBundle(){
    //code for exporting to json and sending to backend
  }
  return (
    <>

      <nav class="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/current-bundles" className="button"><b>Current Bundles</b></Link>
        <Link to="/analytics" className="button"><b>Analytics</b></Link>
      </nav>
      <h1 className="headline">Add Bundles</h1>
      <section>
        <div className="textBlock">
            <div className="addBundle">
              <label for="bundle_name">Enter Bundle Name : </label>
              <input type = "text" id="bundle_name"></input>
              <br></br>
              <label for="bundle_location">Enter Location :          </label>
              <input type = "text" id="bundle_location"></input>
              <br></br>
              <label for="bundle_collectionTime">Enter Bundle Name : </label>
              <input type = "text" id="bundle_collectionTime"></input>
            </div>
            
            <button onClick={addBundle}>Login</button>
        </div>
      </section>
      
      
    </>
  );
}

export default AddBundles
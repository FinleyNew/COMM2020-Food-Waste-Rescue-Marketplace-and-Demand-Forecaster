import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import "./view-tests.css";
import axios from "axios";

function View_tests() {
  const [testData, setTestData] = useState(""); //variable to hold the data gathered from the request, not an array as its one object returned

  const token = localStorage.getItem("token"); //holds the token returned from local storage after logging in, to verify the user
  const API_URL = import.meta.env.VITE_API_URL; //holds the API URL which is in use, can the local host or the deployed version URL

  useEffect(() => { //used a use effect, which automatically updates if the information changes
    axios.get(`${API_URL}/api/v1/admins/tests`, { //get request to retrieve the data
        headers: {
          Authorization: `Bearer ${token}`, //used a header to send the token
        },
      })
      .then((response) => {
        console.log(response.data); //logging the data to display the structure is retrieved in
        setTestData(response.data); //storing the data to display 
      })
      .catch(err => {
           console.log("status:", err.response?.status); //error catching
           console.log("backend error:", err.response?.data);
      });
  }, []);

  return (
    <>
      <div className="deployment">
        <nav className="navRow">
          <Link to="/change-information" className="button">
            Change Information
          </Link>
          <Link to="/view-information" className="button"> {/* navigation buttons to link to the other admin pages */}
            View Information
          </Link>
        </nav>

            {testData && (
              <div className="row">
                <h1 className="header">Passed: {testData.summary.passed}</h1> {/* menu to display the stats of the tests */}
                <h1 className="header">Total: {testData.summary.total}</h1>
                <h1 className="header">Collected: {testData.summary.collected}</h1>
              </div>
            )}
          

          {testData && Array.isArray(testData.collectors) && ( //if there is test data and its in an array
            <div className="container">
            <h2>Collectors</h2>
            <div className="tests">

              {testData.collectors.map((collector, idx) => ( // use a map to display all the elements
                <div key={idx} className="collectorEntry">
                <h3>{collector.nodeid || "(root)"}</h3>
                <p>Outcome: {collector.outcome}</p>

              {/* Show array data */}
              {collector.result && collector.result.length > 0 && (
              <div className="collectorChildren">
                <p>Contents:</p>

                {collector.result.map((item, i) => (
                  <div key={i} className="collectorItem">
                    <p>Node: {item.nodeid}</p>
                    <p>Type: {item.type}</p> {/* show all the elements here */}

                    {/* Some items also have lineno */}
                    {item.lineno && <p>Line: {item.lineno}</p>}
                  </div>
                ))}
              </div>
            )}
        </div>
        ))}
      </div>
    </div>
    )}
      </div>
    </>
  );
}

export default View_tests;
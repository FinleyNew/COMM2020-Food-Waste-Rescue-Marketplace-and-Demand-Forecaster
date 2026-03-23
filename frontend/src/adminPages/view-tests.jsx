import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import "./view-tests.css";
import axios from "axios";

function View_tests() {
  const [testData, setTestData] = useState("");

  const token = localStorage.getItem("token");
  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    axios
      .get(`${API_URL}/api/v1/admins/tests`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        console.log(response.data);
        setTestData(response.data);
      })
      .catch((err) => {
        console.error("Error fetching forecasts:", err);
        alert("No data");
      });
  }, []);

  return (
    <>
      <div className="deployment">
        <nav className="navRow">
          <Link to="/change-information" className="button">
            Change Information
          </Link>
          <Link to="/view-information" className="button">
            View Information
          </Link>
        </nav>


        {testData && (
          <div>
            <h1>Passed: {testData.summary.passed}</h1>
            <h1>Total: {testData.summary.total}</h1>
            <h1>Collected: {testData.summary.collected}</h1>
          </div>
          )}

          {testData && Array.isArray(testData.collectors) && (
  <div className="collectorList">
    <h2>Collectors</h2>

    {testData.collectors.map((collector, idx) => (
      <div key={idx} className="collectorEntry">
        <h3>{collector.nodeid || "(root)"}</h3>
        <p>Outcome: {collector.outcome}</p>

        {/* Show children (result array) */}
        {collector.result && collector.result.length > 0 && (
          <div className="collectorChildren">
            <p>Contents:</p>

            {collector.result.map((item, i) => (
              <div key={i} className="collectorItem">
                <p>Node: {item.nodeid}</p>
                <p>Type: {item.type}</p>

                {/* Some items also have lineno */}
                {item.lineno && <p>Line: {item.lineno}</p>}
              </div>
            ))}
          </div>
        )}
      </div>
    ))}
  </div>
)}
      </div>
    </>
  );
}

export default View_tests;
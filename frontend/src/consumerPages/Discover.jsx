import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import './Discover.css';
import axios from "axios";
import Company from "../assets/Company.png";
import Bundle from "../assets/BundleImage.png";

function Discover() {
  const API_URL = import.meta.env.VITE_API_URL;
  const [bundles, setBundles] = useState([]); // All bundles
  const [query, setQuery] = useState("");     // Search query
  const searchTimeout = useRef(null);         // For debouncing input

  // Fetch all bundles from the backend
  const fetchAllBundles = () => {
    axios.get(`${API_URL}/api/v1/bundles/`, {
      headers: { "Content-Type": "application/json" }
    })
    .then(res => setBundles(res.data))
    .catch(err => console.error("Error fetching bundles:", err));
  };

  // On first load, fetch all bundles
  useEffect(() => {
    fetchAllBundles();
  }, []);

  // Search bundles using the API
  const searchBundles = (searchTerm) => {
    if (!searchTerm) {
      fetchAllBundles();
      return;
    }

    axios.get(`${API_URL}/api/v1/bundles/search/${encodeURIComponent(searchTerm)}`, {
      headers: { "Content-Type": "application/json" }
    })
    .then(response => {
      setBundles(response.data); // Update state with search results
    })
    .catch(err => {
      console.error("Error searching bundles:", err);
      setBundles([]); // Clear bundles if search fails
    });
  };

  // Handle search input change with debounce
  const handleSearchChange = (e) => {
    const value = e.target.value;
    setQuery(value);

    // Clear previous timeout
    clearTimeout(searchTimeout.current);

    // Wait 300ms after typing stops to send request
    searchTimeout.current = setTimeout(() => {
      if (value.trim()) {
        searchBundles(value);
      } else {
        fetchAllBundles(); // If empty, reset to all bundles
      }
    }, 300);
  };

  return (
    <div className="discover">
      <div className="pageHeading">
        <nav className="navRow">
          <Link to="/streaks" className="button"><b>Streaks</b></Link>
          <Link to="/codes" className="button"><b>Codes</b></Link>
        </nav>
        <div className="textHeading">
          <h1>Bundles</h1>
        </div>
      </div>

      <div className="searchRow">
        <p>Search for a Bundle: </p>
        <input
          id="searchBundle"
          type="text"
          placeholder="Search"
          value={query}
          onChange={handleSearchChange}
        />
      </div>

      <div className="bundleList">
        {bundles.map(bundle => (
          <Link to={`/bundle/${bundle.posting_id}`} className="mainBox" key={bundle.posting_id}>
            <div className="bundleEntry">
              <img src={Bundle} alt="Bundle" className="bundleImage" />
              <div className="textBox">
                <div className="bundleRow">
                  <h1>{bundle.category.name || "Bundle Name"}</h1>
                  <h1>{bundle.available} Available</h1>
                </div>
                <div className="bundleRow">
                  <div className="column">
                    <p>Collection Time: {bundle.formatted_time_range}</p>
                    <p>Price: £{bundle.price_display}</p>
                  </div>
                  <img src={bundle.seller.logo_url} alt="Company" className="companyIcon" />
                </div>
              </div>
            </div>
          </Link>
        ))}
        {bundles.length === 0 && <p style={{ color: "red" }}>No bundles found</p>}
      </div>
    </div>
  );
}

export default Discover;
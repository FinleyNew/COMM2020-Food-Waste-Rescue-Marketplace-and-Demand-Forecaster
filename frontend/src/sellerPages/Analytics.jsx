import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import Company from "../assets/Company.png";
import './Analytics.css'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid
} from "recharts";

function Analytics() {
  const API_URL = import.meta.env.VITE_API_URL;
  const [analytics, setAnalytics] = useState([])
  const [noAnalytics, setNoAnalytics] = useState(false);
  const [logo, setLogo] = useState("");
  const [summary, setSummary] = useState("");
  const [collectionPercentages, setCollectionPercentages] = useState("");
  const [discount, setDiscount] = useState([]);
  const [operation, setInsights] = useState([]);
  
  useEffect(() => {
    const token = localStorage.getItem('token');
    axios.get(`${API_URL}/api/v1/sellers/me`,{
      headers:{
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
    .then(response => {
      
      setLogo(response.data.logo_url);
      console.log(logo);
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching bundles:", err);
        
      });

  },[])


  useEffect(() => { //records
    const token = localStorage.getItem('token');
    axios.get(`${API_URL}/api/v1/records/me`,{
      headers:{
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
    .then(response => {
      
      if (response.data.length === 0) {
          setNoAnalytics(true);
        } else {
          setAnalytics(response.data);
          setNoAnalytics(false);
        }
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching bundles:", err);
        alert("No data ");
      });

  },[])

  useEffect(() => { //analytics summary
    const token = localStorage.getItem('token');
    axios.get(`${API_URL}/api/v1/sellers/me/analytics/summary`,{
      headers:{
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
    .then(response => {
      
     setSummary(response.data);
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching bundles:", err);
        alert("No data ");
      });

  },[])


   useEffect(() => { //sell through breakdown
    const token = localStorage.getItem('token');
    axios.get(`${API_URL}/api/v1/sellers/me/analytics/sell-through-breakdown`,{
      headers:{
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
    .then(response => {
      
     setCollectionPercentages(response.data);
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching bundles:", err);
        alert("No data ");
      });

  },[])

  useEffect(() => { //oeprational insights
    const token = localStorage.getItem('token');
    axios.get(`${API_URL}/api/v1/sellers/me/analytics/operational-insights`,{
      headers:{
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
    .then(response => {
      
     setInsights(response.data);
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching bundles:", err);
        alert("No data ");
      });

  },[])

  useEffect(() => { //analytics summary
    const token = localStorage.getItem('token');
    axios.get(`${API_URL}/api/v1/sellers/me/analytics/pricing-effectiveness`,{
      headers:{
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
    .then(response => {
      
     setDiscount(response.data);
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching bundles:", err);
        alert("No data ");
      });

  },[])



  //Calculated totals from arrays retrieved from the backend
  const totalReservations = analytics.reduce(
    (sum,item) => sum + item.observed_reservations,
    0
  );

  const totalNoShows = analytics.reduce(
    (sum, item) => sum + item.observed_no_show,
    0
  );
  const totalWeight = analytics.reduce(
    (sum,item) => sum + item.weight,
    0
  );
  const totalExpired = analytics.reduce(
    (sum,item) => sum + item.observed_expired,
    0
  );

  //Structure for the bar chart displau
  const chartData = [
  {
    name: "Reservations",
    collected: totalReservations,
    noShows: totalNoShows,
    expired: totalExpired
  }
];
  //Maximum scaling the bar chart could use
  const maxValue = Math.max(totalReservations,totalNoShows, totalExpired);



  return (
    <>
      <div className="analytics">
        {/* Initialises the navifation bar where sellers can move between pages */}
        <div className="pageHeading">
          <nav class="navRow">
            <Link to="/current-bundles" className="button"><b>Current Bundles</b></Link>
            <Link to="/add-bundles" className="button"><b>Add Bundles</b></Link>
          </nav>
          
        </div>
          <div className="mainBox">
            <div className="analyticsContent">
              {/* Makes a grid structure with top row containing the company image and circle object with waste prevention stats */}
              <div className="gridRow">
                {/*idx = index */}
                  <BarChart width={300} height={400} data={chartData} style={{ background: "transparent" }}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Legend />

      {/* Same stackId = stacked */}
      <Bar dataKey="collected" stackId="a" fill="#4CAF50" barSize={150} />
      <Bar dataKey="noShows" stackId="a" fill="#fc3d03" barSize={150} />
      <Bar dataKey="expired" stackId="a" fill="#6f00ff" barSize={150} />

    </BarChart>
    <div>
      <p className="desc">Collected - {collectionPercentages.collected_pct_of_posted}%</p>
      <p className="desc">No Shows - {collectionPercentages.no_show_pct_of_posted}%</p>
      <p className="desc">Expired - {collectionPercentages.expired_pct_of_posted}%</p>
    </div>
            <div className="gridColumn">
              <p className="bubbleText">Total Waste Prevented</p>
              <div className="circleObject">
                <img className="circleBubble" 
                  src="https://img.freepik.com/premium-vector/big-green-sun-vector-icon-green-sun-symbol_302321-2439.jpg?semt=ais_user_personalization&w=740&q=80"></img>
                <p className="weight">{totalWeight}kg</p>
              </div>
            </div>
          </div>
        </div>
        <div className="textHeading">
          <h2>Data</h2>
        </div>
        <div className="analyticsContent">
            {/* Desciption entries outputted to screen with the user_id */}
              <h1>Analytics for each bundle</h1>
            <div className="gridRow">
              {analytics.map((analytic, index) => (
          <div key={analytic.posting_id}>
            <div className="desc">
            <h2>Bundle {index + 1}</h2>
            <p className="desc">User ID - {analytic.user_id}</p>
            <p className="desc">Company - Amazon</p>
            <p className="desc">Price - {analytic.price}</p>
            <p className="desc">Category - {analytic.category.name}</p>
            <p className="desc">Reservations - {analytic.observed_reservations}</p>
            <p className="desc">No Shows - {analytic.observed_no_show}</p>
          <p className="desc">Expired - {analytic.observed_expired}</p>
          <p className="desc">Pickup Date - {analytic.pickup_date}</p>
          <p className="desc">Pickup Date Formatted - {analytic.formatted_date}</p>
          <p className="desc">Raining - {analytic.raining.toString()}</p>
            <p className="desc">Weight - {analytic.weight}</p>
          </div>
        </div>
        ))}
          <div>
              <h1>Discount Analytics</h1>
              {discount.map((band, index) => (
                  <div key={index}>
                    <h3>Discount Band {index + 1} — {band.discount_band}%</h3>
                  
                  <p className="desc">Posted Units - {band.posted_units}</p>
                  <p className="desc">Reserved Units - {band.reserved_units}</p>
                    <p className="desc">Collected Units - {band.collected_units}</p>
                  <p className="desc">No Show Units - {band.no_show_units}</p>
                  <p className="desc">Expired Units - {band.expired_units}</p>
                  <p className="desc">Sell Through Rate - {band.sell_through_rate}%</p>
                  <p className="desc">Reservation Conversion Rate - {band.reservation_conversion_rate}%</p>
                  <p className="desc">No Show Rate - {band.no_show_rate}%</p>
              </div>
              
                ))}
            </div>
            <div>
                {/* Operational Insights */}
                {operation.pickup_windows?.map((window, index) => (
                  <div key={index}>
                  <h1>Pickup Window {index + 1} — {window.pickup_window}</h1>
                    <p className="desc">Posted Units - {window.posted_units}</p>
                  <p className="desc">Reserved Units - {window.reserved_units}</p>
                    <p className="desc">Collected Units - {window.collected_units}</p>
                <p className="desc">No Show Units - {window.no_show_units}</p>
                <p className="desc">Expired Units - {window.expired_units}</p>
                <p className="desc">Sell Through Rate - {window.sell_through_rate}%</p>
                <p className="desc">No Show Rate - {window.no_show_rate}%</p>
            </div>
              ))}
              <div>
                {/* Categories */}
                {operation.categories?.map((cat, index) => (
                <div key={index}>
                <h3>Category {index + 1} — {cat.category}</h3>
                <p className="desc">Posted Units - {cat.posted_units}</p>
                <p className="desc">Reserved Units - {cat.reserved_units}</p>
                <p className="desc">Collected Units - {cat.collected_units}</p>
                <p className="desc">Sell Through Rate - {cat.sell_through_rate}%</p>
                </div>
                  ))}
              </div>
            </div>
            <div>
              {/* Best/Worst/Most Popular */}
                <h1>Best Pickup Window by Sell Through</h1>
                <p className="desc">Pickup Window - {operation.best_pickup_window_by_sell_through?.pickup_window}</p>
                <p className="desc">Sell Through Rate - {operation.best_pickup_window_by_sell_through?.sell_through_rate}%</p>

            <h3>Worst Pickup Window by No Show</h3>
            <p className="desc">Pickup Window - {operation.worst_pickup_window_by_no_show?.pickup_window}</p>
            <p className="desc">No Show Rate - {operation.worst_pickup_window_by_no_show?.no_show_rate}%</p>

            <h3>Most Popular Category by Reservations</h3>
            <p className="desc">Category - {operation.most_popular_category_by_reservations?.category}</p>
            <p className="desc">Reserved Units - {operation.most_popular_category_by_reservations?.reserved_units}</p>
            </div>
          </div>
                    <h1>Summary</h1>
                    <div className="gridRow">
                      <div className="gridColumn">
                        <p className="desc">Total Bundles Posted - {summary.total_bundle_postings}</p>
                        <p className="desc">Total Products Posted - {summary.total_posted}</p>
                        <p className="desc">Total Reserved - {summary.total_reserved}</p>
                        <p className="desc">Total Collected - {summary.total_collected}</p>
                        <p className="desc">Total No Shows - {summary.total_no_shows}</p>
                      </div>
                      <div className="gridColumn">
                        <p className="desc">Total Expired - {summary.total_expired}</p>
                        <p className="desc">Reservation Conversion Rate - {summary.reservation_conversion_rate}</p>
                        <p className="desc">Sell Through Rate - {summary.sell_through_rate}</p>
                        <p className="desc">No Show Rate - {summary.no_show_rate}</p>
                        <p className="desc">Expiry Rate - {summary.expiry_rate}</p>
                        <p className="desc">Waste Avoided - {summary.waste_avoided_kg}kg</p>
                      </div>
                    </div>
          <div>
            
          </div>
      </div>
      </div>
    </div>
        {noAnalytics && (
            <p style={{color:"red"}}>
                        No Analytics
                    </p>)}
    </>
  );
}
//exports the component so it can be imported in other files
export default Analytics
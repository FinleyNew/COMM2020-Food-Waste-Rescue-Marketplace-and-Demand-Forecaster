import { Routes, Route, Link } from "react-router-dom";
import './Discover.css'
function Discover() {
  return (
    <>
      <nav class="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/streaks" className="button"><b>Streaks</b></Link>
        <Link to="/codes" className="button"><b>Codes</b></Link>
      </nav>
      <h1 className="headline">Bundles</h1>
      <Link to="/bundle-select" className="sectionPage">
        <section>
          <div className="textBlock">
            <img src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M=" alt="Food" className="leftImg"/>
            <div className="desc">
              <p className="desc">Company Name</p>
              <p className="desc">Category</p>
            </div>
          </div>
          <div className="textBlock">
            <div className="desc">
              <p className="desc">Bundle Name</p>
              <p className="desc">Location</p>
              <p className="desc">Collection Time</p>
            </div>
          </div>
          <div className="formatter">
            <img src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M=" alt="Food" className="thumbnail"/>
              <p className="desc">Company Name</p>
            </div>
          </section>
      </Link>
    </>
  );
}

export default Discover

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
      <section>
        <div className="text-block">
          <p className="desc">Food Item</p>
          <p>Food Item</p>
        </div>
        <div className="formatter">
          <a target="_blank" rel="noopener noreferrer" href="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M=">
          </a>
          <img src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M=" alt="Food" className="thumbnail"/>
            <p>Company Name</p>
        </div>
      </section>
    </>
  );
}

export default Discover

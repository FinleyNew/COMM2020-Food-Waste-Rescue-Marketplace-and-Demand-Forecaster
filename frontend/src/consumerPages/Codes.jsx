import { Routes, Route, Link } from "react-router-dom";
import './Discover.css'
function Codes() {
  let companyName = "Amazon";
  let code = "example code";
  let bundleName = "idk";
  let location = "EX1 2HR";
  let collectionTime = "12:00";
  return (
      <>
        <nav class="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/discover" className="button"><b>Discover</b></Link>
        <Link to="/streaks" className="button"><b>Streaks</b></Link>
      </nav>
      <h1 className="headline">Codes</h1>
      <section>
          <div className="textBlock">
            <img src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M=" alt="Food" className="leftImg"/>
            <div className="desc">
              <p className="desc">{companyName}</p>
              <p className="desc">Bundle Name - {bundleName}</p>
            </div>
          </div>
          <div className="textBlock">
            <div className="desc">
              <p className="codeText">Code - {code}</p>
              <p>Location - {location}</p>
              <p>Collection Time - {collectionTime}</p>
            </div>
          </div>
          </section>
      </>
    );
}

export default Codes

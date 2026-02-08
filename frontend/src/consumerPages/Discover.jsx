import { Routes, Route, Link } from "react-router-dom";
import './Discover.css'
function Discover() {
  let companyName = "Amazon";
  let category = "Fruit";
  let bundleName = "idk";
  let location = "EX1 2HR";
  let collectionTime = "12:00";
  return (
    <>
      <nav class="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/streaks" className="button"><b>Streaks</b></Link>
        <Link to="/codes" className="button"><b>Codes</b></Link>
        <details>
          <summary>
            <img className="setting" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBdndCKhAJ4SlVEaNCkA4U6BN4tDXZsRtxSw&s"></img>
          </summary>
          <label>
            <input type="checkbox" name="darkmode"/>
              Enable Dark Mode DOESNT WORK YET
          </label>
        </details>
      </nav>
      <h1 className="headline">Bundles</h1>
      <Link to="/bundle-select" className="sectionPage">
        <section>
          <div className="textBlock">
            <img src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M=" alt="Food" className="leftImg"/>
            <div className="desc">
              <p className="desc">{companyName}</p>
              <p className="desc">{category}</p>
            </div>
          </div>
          <div className="textBlock">
            <div className="desc">
              <p className="desc">Bundle Name - {bundleName}</p>
              <p className="desc">Location - {location}</p>
              <p className="desc">Collection Time - {collectionTime}</p>
            </div>
          </div>
          <div className="formatter">
            <img src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M=" alt="Food" className="thumbnail"/>
              <p className="desc">{companyName}</p>
            </div>
          </section>
      </Link>
    </>
  );
}

export default Discover

import { Routes, Route, Link } from "react-router-dom";
import {useState} from "react"
function BundleSelect() {
  let companyName = "Amazon";
  let category = "Fruit";
  let bundleName = "idk";
  let location = "EX1 2HR";
  let collectionTime = "12:00";
  let allergens = "none";
  const [Popup, setPopup] = useState(false);
  function openPopup(){
    setPopup(true);
  }
  function closePopup(){
    setPopup(false);
  }
  return (
      <>
       <nav className="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/discover" className="button"><b>Discover</b></Link>
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
      <section>
        <div className="textBlock">
          <img src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M=" alt="Food" className="leftImg"/>
          <div className="desc">
            <p className="desc">Company - {companyName}</p>
            <p className="desc">Category - {category}</p>
          </div>
        </div>
        <div className="textBlock">
          <div className="desc">
            <p className="desc">Bundle Name - {bundleName}</p>
            <p className="desc">Location - {location}</p>
            <p className="desc">Collection Time - {collectionTime}</p>
            <p className="desc">Allergens - {allergens}</p>
          </div>
        </div>
        <div className="formatter">
          <img src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M=" alt="Food" className="thumbnail"/>
            <p className="desc">Company Name - {companyName}</p>
          </div>
        <div className="formatter">
          <button>+</button>
          <button>-</button>
          <button className="button" onClick={openPopup}>Pay</button>
          {Popup &&(
            <div className="popup open-popup" id="payment">
              <h1>Payment Successful!</h1>
              <button className="button" onClick={closePopup}>Confirm</button>
            </div>
          )}
        </div>
        </section>
      </>
    );
}
export default BundleSelect;
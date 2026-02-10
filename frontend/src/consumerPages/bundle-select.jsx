import { Link, useParams } from "react-router-dom";
import { useState, useEffect } from "react";

function BundleSelect() {

  const { id } = useParams();

  const [bundle, setBundle] = useState(null);
  const [Popup, setPopup] = useState(false);

  function openPopup() {
    setPopup(true);
  }

  function closePopup() {
    setPopup(false);
  }

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/v1/bundles/${id}`)
      .then(res => res.json())
      .then(data => {
        console.log("Bundle data:", data);
        setBundle(data);
      })
      .catch(err => console.error(err));
  }, [id]);

  if (!bundle) return <p>Loading bundle...</p>;

  return (
    <>
      <nav className="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/discover" className="button"><b>Discover</b></Link>
        <Link to="/streaks" className="button"><b>Streaks</b></Link>
        <Link to="/codes" className="button"><b>Codes</b></Link>

        <details>
          <summary>
            <img
              className="setting"
              src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBdndCKhAJ4SlVEaNCkA4U6BN4tDXZsRtxSw&s"
              alt="settings"
            />
          </summary>
          <label>
            <input type="checkbox" name="darkmode" />
            Enable Dark Mode DOESNT WORK YET
          </label>
        </details>
      </nav>

      <h1 className="headline">Bundles</h1>

      <section>
        <div className="textBlock">
          <img
            src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M="
            alt="Food"
            className="leftImg"
          />
          <div className="desc">
            <p className="desc">Category - {bundle.category}</p>
            <p className="desc">Allergens - {bundle.allergens}</p>
          </div>
        </div>

        <div className="textBlock">
          <div className="desc">
            <p className="desc">Bundle Name - {bundle.bundleName}</p>
            <p className="desc">Location - {bundle.location}</p>
            <p className="desc">Collection Time - {bundle.collectionTime}</p>
            <p className="desc">Allergens - {bundle.allergens}</p>
          </div>
        </div>

        <div className="formatter">
          <img
            src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M="
            alt="Food"
            className="thumbnail"
          />
          <p className="desc">Company Name - {bundle.companyName}</p>
        </div>

        <div className="formatter">
          <button>+</button>
          <button>-</button>

          <button className="button" onClick={openPopup}>Pay</button>

          {Popup && (
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

import { Link, useParams } from "react-router-dom"; //to use the buttons to change to other pages
import { useState, useEffect } from "react"; //to use the fetch, to make sure it only fetches once
import './Discover.css'
import Company from "../Assets/Company.png";
import Bundle from "../Assets/Bundleimage.png";
function BundleSelect() {

  const { id } = useParams();

  const [bundle, setBundle] = useState(null); //bundle is used to hold the data, setBundle is used to store it
  const [Popup, setPopup] = useState(false);

  function openPopup() {
    setPopup(true); //if variable is true then popUp needs to be opened 
  }

  function closePopup() {
    setPopup(false); //if variable is false then popUp needs to be closed
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


  function createReservation(postingID){
    const token = localStorage.getItem(`token`);
    const payload = JSON.parse(atob(token.split('.')[1]));
    const userID = parseInt(payload.sub);
    /*const data = {
      posting_id : postingID,
      user_id: userID
    };*/
    //console.log("Creating reservation with:", data);
    console.log("Sending reservation: ", {postingID,userID});
    
    fetch("http://127.0.0.1:8000/api/v1/reservations/", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        posting_id:postingID,
        user_id:userID
      })
    })
      .then(async res => {
        const data = await res.json();

        if(!res.ok){
          console.error("reservation failed",data);
          return;
        }
        console.log("reservation created",data);
      })
      .catch(err => console.error("Error : ",err));
    
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
        <div className="bundleEntry">
          <div className="textBlock">
            <img
              src={Company}
              alt="Company"
              className="leftImg"
            />
            <div className="desc">
              <p className="desc">Category - {bundle.category}</p>
              <p className="desc">Allergens - {bundle.allergens}</p>
              <p classname="desc">Price - £{bundle.price}</p>
            </div>
          </div>

          <div className="textBlock">
            <div className="desc">
              <p className="desc">Collection Time - {bundle.end_time}</p>
              <p className="desc">Allergens - {bundle.allergens}</p>
            </div>
          </div>

          <div className="formatter">
            <img
              src={Bundle}
              alt="Bundle"
              className="thumbnail"
            />
            <br></br>
            <div className="formatter">
            <button className="button" onClick={() => (openPopup(),createReservation(bundle.posting_id))}>
              Pay
            </button>

            {Popup && (
              <div className="popup open-popup" id="payment">
                <h1>Payment Successful!</h1>
                <button className="button" onClick={closePopup}>Confirm</button>
              </div>
            )}
          </div>
            {/*<p className="desc">Company Name - {bundle.companyName}</p>*/}
          </div>
        </div>
      </section>
    </>
  );
}

export default BundleSelect;

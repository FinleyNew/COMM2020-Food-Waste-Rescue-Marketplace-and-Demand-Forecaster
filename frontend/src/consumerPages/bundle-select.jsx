import { Link, useParams } from "react-router-dom"; //to use the buttons to change to other pages
import { useState, useEffect } from "react"; //to use the fetch, to make sure it only fetches once
import './Discover.css' //links to the css page to move and size different components around
import Company from "../assets/Company.png";
import Bundle from "../assets/Bundleimage.png"; //here for the base images
function BundleSelect() {

  const { id } = useParams(); //creates the ID variable to store the bundleID to navigate pages with it

  const [bundle, setBundle] = useState(null); //bundle is used to hold the data, setBundle is used to store it
  const [Popup, setPopup] = useState(false);

  function openPopup() {
    setPopup(true); //if variable is true then popUp needs to be opened 
  }

  function closePopup() {
    setPopup(false); //if variable is false then popUp needs to be closed
  }

  useEffect(() => { //useEffect allows the command run on entering the page and if anything happens inside ID
    fetch(`http://127.0.0.1:8000/api/v1/bundles/${id}`) //links to the backend page on the API with the specific bundle of ID
      .then(res => res.json()) //converts the response into JSON Data
      .then(data => { //data is the bundle object
        setBundle(data); //updates the react state so the page can rerender with the new info
      })
      .catch(err => console.error(err)); //catches any errors
  }, [id]); //this part means if ID changes the page reloades with the new information

  if (!bundle) return <p>Loading bundle...</p>;


  function createReservation(postingID){ //this function takes place if the user "pays" for a bundle
    const token = localStorage.getItem(`token`); //gets the users token, for security and to make sure the site gets THEIR information
    const payload = JSON.parse(atob(token.split('.')[1])); //gets the exact payload from the token, rather than the bundle information, more accurate, the split gets the ...
    const userID = parseInt(payload.sub); // ... part that contains the userID then using sub gets the userID
    
    
    
    fetch("http://127.0.0.1:8000/api/v1/reservations/", {
      method: "POST", //have to define POST as GET is the default, means we are sending data as a priority rather than getting it
      headers: { //extra data we are sending to the backend
        "Authorization": `Bearer ${token}`, //verifies the users as who they are and their token
        "Content-Type": "application/json" //telling the backend we are explicity sending JSON data
      },
      body: JSON.stringify({ //with sending the data its different as we have to convert it to a JSON string to send it to the backend server 
        posting_id:postingID,
        user_id:userID
      })
    })
      .then(async res => {
        const data = await res.json(); //waits to check if the data was sent

        if(!res.ok){ //if it sent
          console.error("reservation failed",data); //display that the reservation failed due to an error
          return; //return back to the page
        }
        console.log("reservation created",data); //if else display that the data sent 
      })
      .catch(err => console.error("Error : ",err));
    
  }


  return (
    <>
      <nav className="row">
        <Link to="/login" className="button"><b>Login Page</b></Link> {/*This section holds all the links to the other pages and the settings page*/}
        <Link to="/discover" className="button"><b>Discover</b></Link>
        <Link to="/streaks" className="button"><b>Streaks</b></Link>
        <Link to="/codes" className="button"><b>Codes</b></Link>

        <details>
          <summary>
            <img
              className="setting"
              src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBdndCKhAJ4SlVEaNCkA4U6BN4tDXZsRtxSw&s" //image for the settings page
              alt="settings"
            />
          </summary>
          <label>
            <input type="checkbox" name="darkmode" />
            Enable Dark Mode DOESNT WORK YET
          </label>
        </details>
      </nav>

      <h1 className="headline">Bundles</h1> {/* header for the bundles page */}

      <section>
        <div className="bundleEntry"> {/* the start for each bundle and inside this div holds all the info for the bundle */}
          <div className="textBlock">
            <img
              src={Company}
              alt="Company"
              className="leftImg" 
            />{/* holds the base company image */}
            <div className="desc">
              <p className="desc">Category - {bundle.category}</p> {/* displays the category, allergens and prices */}
              <p className="desc">Allergens - {bundle.allergens}</p>
              <p classname="desc">Price - £{bundle.price}</p>
            </div>
          </div>

          <div className="textBlock"> {/* each textbox defines a new rox for the bundle rectangle display  */}
            <div className="desc">
              <p className="desc">Date to Collect - {bundle.formatted_date}</p> {/* displays the formatted date and the time range */}
              <p className="desc">Time to Collect - {bundle.formatted_time_range}</p>
            </div>
          </div>

          <div className="formatter">
            <img
              src={Bundle}
              alt="Bundle"
              className="thumbnail" //holds the specific bundle image
            />
            <br></br>
            <div className="formatter">
            <button className="button" onClick={() => (openPopup(),createReservation(bundle.posting_id))}> {/* if the pay button is clicked it sends the information to the create reservation page */}
              Pay
            </button>

            {Popup && (
              <div className="popup open-popup" id="payment">
                <h1>Payment Successful!</h1>  {/*if the button is clicked, open the pop up to pay*/}
                <button className="button" onClick={closePopup}>Confirm</button>
              </div>
            )}
          </div>
           
          </div>
        </div>
      </section>
    </>
  );
}

export default BundleSelect; //exports the component so it can be imported in other files

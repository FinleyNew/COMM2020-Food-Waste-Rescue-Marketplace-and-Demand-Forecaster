import { Routes, Route, Link } from "react-router-dom";
import "./loginPage.css"
function Unauthorised() {
  return(
    <>
      {/* Gives a clickable link to redirect back to the login page */}
      {/* Ouputs a message explaining the user lacks authorisation */}
      <div className="loginPage">
        <div className="loginBox">
          <div className="authenticateItems">
            <h1>You are unauthorised to view this page, please log in with another account </h1>
            <nav> 
                <Link to="/login" class="authenticateButton">Login Page</Link>
            </nav>
          </div>
        </div>
      </div> 

    </>
    
  );
}

export default Unauthorised; //exports the component so it can be imported in other files
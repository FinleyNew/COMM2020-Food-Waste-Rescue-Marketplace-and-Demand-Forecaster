import { Routes, Route, Link } from "react-router-dom";
function Unauthorised() {
  return(
    <>
      {/* Gives a clickable link to redirect back to the login page */}
      <nav> 
          <Link to="/login">Login Page</Link>
      </nav>
      {/* Ouputs a message explaining the user lacks authorisation */}
      <h1>You are unauthorised to view this page, please log in with another account </h1> 

    </>
    
  );

}

export default Unauthorised; //exports the component so it can be imported in other files
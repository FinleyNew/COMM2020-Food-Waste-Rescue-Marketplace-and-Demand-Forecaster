import { Routes, Route, Link } from "react-router-dom";
import "../HomePage.css" //Imports the css file that defines class structures
function Home() {
  return (
    <div className="homePage">
      <nav>
        
        <Link to="/login">LoginPage</Link> {/*Creates a link that directs to the login page when clicked reading LoginPage*/}
        
      </nav>
      
      <h1>Home Page</h1> {/*Adds text displaying the login page title*/}
      
    </div>
  );
}

export default Home; //exports the component so it can be imported in other files

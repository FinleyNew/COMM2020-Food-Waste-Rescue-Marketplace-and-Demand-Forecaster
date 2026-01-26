import { Routes, Route, Link } from "react-router-dom";
import "../HomePage.css"
function Home() {
  return (
    <div>
      <nav>
        
        <Link to="/login">LoginPage</Link>
        
      </nav>
      <h1>Home Page</h1>
      <h2>Fridge Raiders! ©</h2>
    </div>
  );
}

export default Home;

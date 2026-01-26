import { Routes, Route, Link } from "react-router-dom";
function Home() {
  return (
    <div>
      <nav>
        
        <Link to="/login">LoginPage</Link>
        
      </nav>
      <h1>Home Page</h1>
    </div>
  );
}

export default Home;

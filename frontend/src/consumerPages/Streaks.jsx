import { Routes, Route, Link } from "react-router-dom";
import './Discover.css'
function Streaks() {
  return (
      <>
        <nav class="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/discover" className="button"><b>Discover</b></Link>
        <Link to="/codes" className="button"><b>Codes</b></Link>
      </nav>
      <h1 className="headline">Streaks</h1>
      <p className="textCentre">You have rescued for __ weeks in a row!</p><hr></hr>
      <div className="rowIcons">
        <p className="headline">Badges:</p>
        <img className="icon" src="https://thumbs.dreamstime.com/b/modern-bronze-circle-metal-badges-labels-design-elements-vector-illustration-84952346.jpg" alt="Bronze Badge"/>   
        <img className="icon" src="https://img.favpng.com/11/16/23/gold-medal-silver-medal-illustration-png-favpng-vJK1hRCuK1bUdtG0Hb4dJ7VkU.jpg" alt="Silver Badge"/>   
        <img className="icon" src="https://www.onlygfx.com/wp-content/uploads/2022/04/blank-gold-badge-label-2.png" alt="Gold Badge"/>   
      </div>
      <hr></hr>
      <p>Summary PIS</p>
        </>
    );
}

export default Streaks;

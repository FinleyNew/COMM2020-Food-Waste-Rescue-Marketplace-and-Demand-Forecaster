import { Routes, Route, Link } from "react-router-dom";
function CurrentBundles() {
  let companyName = "Amazon";
  let category = "Fruit";
  let bundleName = "idk";
  let location = "EX1 2HR";
  let collectionTime = "12:00";
  return (
    <>
    
      <nav class="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/add-bundles" className="button"><b>Add Bundles</b></Link>
        <Link to="/analytics" className="button"><b>Analytics</b></Link>
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
          </div>
        </div>
        <div className="formatter">
          <img src="https://media.istockphoto.com/id/1457433817/photo/group-of-healthy-food-for-flexitarian-diet.jpg?s=612x612&w=0&k=20&c=v48RE0ZNWpMZOlSp13KdF1yFDmidorO2pZTu2Idmd3M=" alt="Food" className="thumbnail"/>
            <p className="desc">Company Name - {companyName}</p>
          </div>
        <div className="formatter">
          <p className="button">Edit</p> 
          <p className="button">Delete</p>
        </div>
        </section>
    </>
  );
}

export default CurrentBundles
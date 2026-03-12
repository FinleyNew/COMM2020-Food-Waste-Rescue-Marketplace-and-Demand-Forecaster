import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./loginPage.css"


function LoginPage({setUser}) {// username is the variable, setUsername changes it and useState means it can be changed throughout the program
  const [username, setUsername] = useState(""); //setUsername is the function to change it, defining variables of username and password
  const [password, setPassword] = useState(""); //more secure than accessing it with getElementId
  const [confirmPassword, checkPassword] = useState("");
  const navigate = useNavigate();
  const [ErrorLogin, setErrorLogin] = useState(false);
  const [Popup, setPopup] = useState(false);
  const [token,setToken] = useState("");
  const [role,setRole] = useState("");
  const [accountType, setAccountType] = useState("Consumer");
  const[displayName, setDisplayName] = useState("");
  const [location, setLocation] = useState("");
  const [openingHours, setOpeningHours] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [showPassword, setShowPassword] = useState("");
  const [openingTime, setOpeningTime] = useState("");
  const [closingTime, setClosingTime] = useState("");
  //let invalidTime = false;
  const timeRegex = /^([01]\d|2[0-3]):[0-5]\d$/;
  const emailRegex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
  const toMinutes = (time) => {
    const [hours, minutes] = time.split(":").map(Number);
    return hours * 60 + minutes;
  }

  const validTimeFormat =
    timeRegex.test(openingTime) &&
    timeRegex.test(closingTime);

  const invalidTime =
    accountType === "Seller" &&
    validTimeFormat &&
    toMinutes(closingTime) <= toMinutes(openingTime);


  
  const validTime =
    timeRegex.test(openingTime) &&
    timeRegex.test(closingTime) &&
    toMinutes(closingTime) > toMinutes(openingTime);
  const API_URL = import.meta.env.VITE_API_URL;


  const handleAccountTypeChange = (e) => {
    const value = e.target.value;
    setAccountType(value);

    setUsername("");
    setPassword("");
    checkPassword("");
    setRole("");
    setDisplayName("");
    setLocation("");
    setCompanyName("");

  }

  const handleCancel = () => {
    setUsername("");
    setPassword("");
    checkPassword("");
    setRole("");
    setDisplayName("");
    setLocation("");
    setCompanyName("");

    closePopup();
  }

  const handleAccountCreation = () => {
    setUsername("");
    setPassword("");
    

    closePopup();
  }


  function openPopup() {
    setPopup(true); //if variable is true then popUp needs to be opened 
  }
  function closePopup() {
    setPopup(false); //if variable is false then popUp needs to be closed
  }
  function loginFunction() {

    const data={
      grant_type:"password",
      username:username,
      password:password.toString()
    };
    const formData = new URLSearchParams();
    formData.append("grant_type","password");
    formData.append("username",username);
    formData.append("password",password);
   
    console.log(import.meta.env);


    
    axios.post(`${API_URL}/api/v1/login/access-token`, formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    }
    })
    .then(response => {

    const token = response.data.access_token;
    setToken(token);
    if (token) {

      axios.get(`${API_URL}/api/v1/users/me`, {
      headers: {
        "Authorization": `Bearer ${token}`
      }
      })
      .then(response => {

        const role = response.data.role;
        setRole(role);

        if (role === "consumer") {
          setUser({
            username: username,
            role: "consumer"
          });

          localStorage.setItem("token", token);
          navigate("/discover");

        } else if (role === "seller") {
          setUser({
            username: username,
            role: "seller"
          });

          localStorage.setItem("token", token);
          navigate("/current-bundles");

        } else {
          console.error("unknown role");
        }

      })
      .catch(err => console.error(err));
    }

    })
    .catch(err => {
      console.error("Error fetching data", err);
      alert("No data");
    });

  }
  function createAccount(){

    //combine times
    


    if(accountType==="Consumer"){
      const data = {
        consumer_in: {
          display_name: displayName
        },
        user_in: {
          email: username,
          password: password
        }
      }

      axios.post(`${API_URL}/api/v1/consumers/`, data, {
          headers: {
            
            "Content-Type": "application/json"
          }
          })
          .then(response => {
              console.log("profile made");
              navigate("/login")
              closePopup()
          })
          .catch(err => {
            console.error("Request failed:", err);
          });




    }
    else if(accountType==="Seller"){
      const data = {
        seller_in: {
          name: companyName,
          location: location,
          opening_hours: `${openingTime} - ${closingTime}`
        },
        user_in: {
          email: username,
          password: password
        }
      }
      console.log(data);

      

        axios.post(`${API_URL}/api/v1/sellers/`, data, {
          headers: {
            "Content-Type": "application/json"
          }
          })
          .then(response => {
              console.log(data);
              navigate("/login")
              closePopup()
          })
          .catch(err => {
            console.log("status:", err.response.status);
            console.log("backend error:", err.response.data);
          });
      
      
      handleAccountCreation();




    }
    else{
      //idk some error
    }
  }

  return (
    <div className="loginBox">
      <div className="loginItems">
        <h3>Please Enter Your Email and Password</h3> {/* Writes a prompt to screen for username and password */}
        {/* Creates an input box for the user to send their username and saves it */}
        <div className="rowRegister">
          <p>Email:</p>
          <input 
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        {/* Creates an input box for the user to send their password and saves it */}
        <div className="rowRegister">
          <p>Password:</p>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        {ErrorLogin && (
          <div className="popupRegister open-popupRegister">
            <h3>No Account Found</h3>
            <br></br>
            <br></br>
            <p>We could not find an account associated with this email and password, please try again.</p>
            <br></br>
            <button onClick={() => setErrorLogin(false)}>Confirm</button>
          </div>
        )}
        <br></br>
        {/* Makes a button that submits entires to above input boxes when selected*/}
        <div className="rowRegister">
          <button className="loginButton" onClick={loginFunction}>Login</button>
          <button className="loginButton" onClick={() => (openPopup())}> {/* if the pay button is clicked it sends the information to the create reservation page */}
                Register
          </button>
        </div>



            {Popup && (
              <div className="popupRegister open-popupRegister">
                <h3>Account Registration</h3>
                <br></br>
                <div classname="rowRegister">
                  <label for="user">Choose Account Type: </label>
                  <select
                    name="user"
                    id="user"
                    value={accountType} onChange={handleAccountTypeChange}
                    
                  >
                    <option value="Consumer">Consumer</option>
                    <option value="Seller">Seller</option>
                  </select>
                </div>
                <div className="rowRegister">
                  <p>Email: </p>
                  <input 
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                  />
                </div>
                {accountType === "Consumer" && (
                  <>
                  <div classname="rowRegister">
                  <p>Display Name: </p>
                  <input
                    type="text"
                    value={displayName}
                    onChange={(e) => setDisplayName(e.target.value)}
                    />
                </div>
                  </>
                )}
                {accountType==="Seller" && (
                  <>
                  <div classname="rowRegister">
                  <p>Name: </p>
                  <input
                    type="text"
                    value={companyName}
                    onChange={(e) => setCompanyName(e.target.value)}
                    />
                </div>
                  <div classname="rowRegister">
                  <p>Location: </p>
                  <input
                    type="text"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    />
                </div>
                <div classname="rowRegister">
                  <p>Opening Time : </p>
                  <input
                    type="text"
                    value={openingTime}
                    onChange={(e) => setOpeningTime(e.target.value)}
                    />
                </div>
                <div classname="rowRegister">
                  <p>Closing Time : </p>
                  <input
                    type="text"
                    value={closingTime}
                    onChange={(e) => setClosingTime(e.target.value)}
                    />
                </div>
                  </>
                   
                )}
                {username && !emailRegex.test(username) && (
                  <p style={{color: "red"}}>Email must contain @</p>
                ) }
                
                {confirmPassword && password !== confirmPassword && (
                  <p style={{color: "red"}}>Passwords do not match</p>
                )}
               {openingTime && !timeRegex.test(openingTime) && (
                  <p style={{color:"red"}}>
                      Times must be in format HH:MM
                  </p>
                )}
                {closingTime && !timeRegex.test(closingTime) && (
                  <p style={{color:"red"}}>
                      Times must be in format HH:MM
                  </p>
                )}
                {accountType==="Seller" && invalidTime && (
                  <p style={{color:"red"}}>
                      Invalid Time, Opening Time cannot be before Closing Time
                  </p>
                )}
                
                {/* Creates an input box for the user to send their password and saves it */}
                <div className="rowRegister">
                  <p>Password:</p>
                  <input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </div>
                <div className="rowRegister">
                  <p>Confirm Password:</p>
                  <input
                    type={showPassword ? "text" : "password"}
                    value={confirmPassword}
                    onChange={(e) => checkPassword(e.target.value)}
                  />
                </div>
                <button onClick={() => setShowPassword(!showPassword)}>
                  {showPassword ? "Hide " : "Show"} Password
                </button>
                <div className="rowRegister">
                  <button onClick={createAccount} //was close popup
                            disabled={password!==confirmPassword || !validTimeFormat || invalidTime}
                            >Create Account</button>
                  <button onClick={handleCancel}>Cancel</button>
                </div>
              </div>
            )}




      </div>
    </div>
  );
}

//exports the component so it can be imported in other files
export default LoginPage;

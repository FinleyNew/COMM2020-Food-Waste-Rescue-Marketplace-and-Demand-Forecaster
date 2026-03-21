import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./loginPage.css"


function LoginPage({setUser}) {// username is the variable, setUsername changes it and useState means it can be changed throughout the program
  const [username, setUsername] = useState(""); //setUsername is the function to change it, defining variables of username and password
  const [password, setPassword] = useState(""); //more secure than accessing it with getElementId
  const [confirmPassword, checkPassword] = useState("");
  const navigate = useNavigate();
  
  const [Popup, setPopup] = useState(false);
  const [token,setToken] = useState("");
  const [role,setRole] = useState("");
  const [accountType, setAccountType] = useState("Consumer");
  const [displayName, setDisplayName] = useState("");
  const [location, setLocation] = useState("");
  const [openingHours, setOpeningHours] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [showPassword, setShowPassword] = useState("");
  const [openingTime, setOpeningTime] = useState("");
  const [closingTime, setClosingTime] = useState("");
  //let invalidTime = false;
  const timeRegex = /^([01]\d|2[0-3]):[0-5]\d$/;
  const emailRegex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
  const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{6,}$/;
  const [accountError, setAccountError] = useState(""); // <-- new
  const [loginError, setLoginError] = useState(""); // <-- new
  

  const validPassword = passwordRegex.test(password);
  const [agree, setAgree] = useState(false);
  const [conditions, setConditions] = useState(false);

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

  const timeValidForSeller = 
    accountType==="Seller"
    ? validTimeFormat && toMinutes(closingTime) > toMinutes(openingTime)
    : true;

  
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
    setAccountError("");

  }

  const handleCancel = () => {
    setUsername("");
    setPassword("");
    checkPassword("");
    setRole("");
    setDisplayName("");
    setLocation("");
    setCompanyName("");
    setAccountError("");

    closePopup();
  }

  const handleAccountCreation = () => {
    setUsername("");
    setPassword("");
    checkPassword("");
    setRole("");
    setDisplayName("");
    setLocation("");
    setCompanyName("");
    setOpeningTime("");
    setClosingTime("");
    setAccountError("");
    

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
          const userObj = { username: username, role: "consumer" }
          setUser(userObj)
          localStorage.setItem("user", JSON.stringify(userObj))
          localStorage.setItem("token", token);
          
          navigate("/discover");

        } else if (role === "seller") {
          const userObj = { username: username, role: "seller" }
          setUser(userObj)
          localStorage.setItem("user", JSON.stringify(userObj))
          localStorage.setItem("token", token);
          
          console.log(openingHours);
          navigate("/current-bundles");

        } else {
          const userObj = { username: username, role: "admin" }
          setUser(userObj)
          localStorage.setItem("user", JSON.stringify(userObj))
          localStorage.setItem("token", token);
          navigate("/view-information");
        }

      })
      .catch(err => {
           console.log("status:", err.response?.status);
           console.log("backend error:", err.response?.data);

            
              });
    }

    })
     .catch(err => {
           console.log("status:", err.response?.status);
           console.log("backend error:", err.response?.data);

             if(err.response?.status === 401 && err.response?.data?.detail){
                setLoginError(err.response.data.detail);
              } else {
                setLoginError("An unexpected error occurred. Please try again.");
                } 
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
              handleAccountCreation();
              closePopup()
          })
          .catch(err => {
           console.log("status:", err.response?.status);
           console.log("backend error:", err.response?.data);

             if(err.response?.status === 400 && err.response?.data?.detail){
                setAccountError(err.response.data.detail);
              } else {
                setAccountError("An unexpected error occurred. Please try again.");
                } 
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
              handleAccountCreation();
              closePopup()
          })
          .catch(err => {
           console.log("status:", err.response?.status);
           console.log("backend error:", err.response?.data);

             if(err.response?.status === 400 && err.response?.data?.detail){
                setAccountError(err.response.data.detail);
              } else {
                setAccountError("An unexpected error occurred. Please try again.");
                } 
              });
    }
    else{
      //idk some error
    }
  }

  return (
    <div className="loginPage">
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
          {loginError && (
            <div className="popupRegister open-popupRegister">
              <h3>No Account Found</h3>
              <br></br>
              <br></br>
              <p>We could not find an account associated with this email and password, please try again.</p>
              <br></br>
              <button onClick={() => setLoginError("")}>Confirm</button>
            </div>
          )}
          <br></br>
          {/* Makes a button that submits entires to above input boxes when selected*/}
          <div className="rowRegister">
            <button className="loginButton" onClick={loginFunction}>Login</button>
            <button className="loginButton" onClick={() => (openPopup(""))}> {/* if the pay button is clicked it sends the information to the create reservation page */}
                  Register
            </button>
          </div>
              {Popup && (
                <div className="popupRegister open-popupRegister">
                  <h3>Account Registration</h3>
                  <br></br>
                  <div className="rowRegister">
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
                  <br></br>
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
                    <div className="rowRegister">
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
                    <div className="rowRegister">
                    <p>Name: </p>
                    <input
                      type="text"
                      value={companyName}
                      onChange={(e) => setCompanyName(e.target.value)}
                      />
                  </div>
                    <div className="rowRegister">
                    <p>Location: </p>
                    <input
                      type="text"
                      value={location}
                      onChange={(e) => setLocation(e.target.value)}
                      />
                  </div>
                  <div className="rowRegister">
                    <p>Opening Time : </p>
                    <input
                      type="text"
                      value={openingTime}
                      onChange={(e) => setOpeningTime(e.target.value)}
                      />
                  </div>
                  <div className="rowRegister">
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
                    <p style={{color: "red"}}>Email must contain @ and contain a domain name</p>
                  ) }
                  {password && !passwordRegex.test(password) && (
                    <p style={{color: "red"}}>Password must contain at least 6 characters, 1 capital letter, 1 number and 1 special character</p>
                  )}
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
                  {accountError && (
                    <p style={{ color: "red", marginBottom: "10px" }}>
                        {accountError}
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
                  <input
                    type="checkbox"
                    id="showPassword"
                    onChange={() => setShowPassword(!showPassword)}
                  />
                  <label for="showPassword">{showPassword ? "Hide " : "Show"} Password</label>
                  <br></br><br></br>
                  <input
                    type="checkbox"
                    id="conditions"
                    onChange={() => setAgree(!agree)}
                  />
                  <label>Agree to the <a className="terms" onClick={()=>setConditions(true)}>terms and conditions</a></label>
                  {conditions && (
                    <div className="popupRegister open-popupRegister">
                    <h3>Terms and Conditions</h3>
                    <div className="scrollBox">
                      <p>Last Updated: 16/03/2026</p>
                      <p>Platform name: tlll.me</p>
                      <h3>1. Introduction</h3>
                      <p>These Terms and Conditions govern access to and use of the tlll.com web application. tlll.com is an educational software platform designed to reduce food waste by allowing sellers to list surplus food bundles and consumers to reserve those bundles for collection. By creating an account, accessing the platform, or using any part of the service, you agree to these Terms.</p>
                      <h3>2. About the Platform</h3>
                      <p>tlll.com provides a digital marketplace and reservation service for surplus food bundles. The platform allows:</p>
                      <ul>
                        <li>Sellers to create and manage bundle listings</li>
                        <li>Consumers to browse and reserve bundles</li>
                        <li>Sellers and consumers to interact through reservation, pickup, and issue reporting</li>
                        <li>Developers to oversee platform operation</li>
                      </ul>
                      <p>The platform facilitates reservations and collection workflows, including claim-code verification, but does not itself prepare, inspect, or physically distribute food.</p>
                      <h3>3. User Roles</h3>
                      <p>Users may be assigned one of the following roles:</p>
                      <p>Consumer</p>
                      <p>A consumer may browse available bundles, reserve bundles, view claim codes, and manage their own reservations.</p>
                      <p>Seller</p>
                      <p>A seller may create and manage bundle listings, monitor reservation outcomes, validate claim codes, and respond to relevant reports or operational issues.</p>
                      <p>Developer</p>
                      <p>A maintainer may oversee the proper operation of the platform, review reports, and manage platform-wide data or access where necessary.</p>
                      <p>Users must only use the parts of the platform associated with their authorised role.</p>
                      <h3>4. Account Responsibilities</h3>
                      <p>You are responsible for:</p>
                      <ul>
                        <li>Providing accurate account information</li>
                        <li>Keeping your login credentials secure</li>
                        <li>Ensuring that your use of the platform is lawful and honest</li>
                        <li>All activity carried out through your account</li>
                      </ul>
                      <p>You must not:</p>
                      <ul>
                        <li>Impersonate another person or organisation</li>
                        <li>Create misleading accounts</li>
                        <li>Attempt to gain unauthorised access to another role’s pages or data</li>
                        <li>Misuse platform features, reports, or reservation systems</li>
                      </ul>
                      <p>We may suspend or restrict accounts that violate these Terms.</p>
                      <h3>5. Seller Obligations</h3>
                      <p>If you use the platform as a seller, you agree to:</p>
                      <ul>
                        <li>Provide accurate listing information, including bundle description, category, price, allergens, weight, and pickup window</li>
                        <li>Ensure bundle quantities are truthful and not misleading</li>
                        <li>Honour valid reservations where possible</li>
                        <li>Use claim-code collection procedures correctly</li>
                        <li>Update listing and reservation statuses honestly</li>
                        <li>Respond appropriately to issue reports where required</li>
                      </ul>
                      <p>Sellers are responsible for the accuracy of bundle information they provide.</p>
                      <h3>6. Consumer Obligations</h3>
                      <p>If you use the platform as a consumer, you agree to:</p>
                      <ul>
                        <li>Reserve bundles only when you genuinely intend to collect them</li>
                        <li>Collect bundles within the specified pickup window</li>
                        <li>Present the correct claim code where required for collection</li>
                        <li>Review listing information carefully before making a reservation</li>
                        <li>Behave respectfully toward sellers and other users</li>
                      </ul>
                      <p>Failure to collect a reserved bundle within the stated collection period may result in the reservation being marked as expired or as a no-show under platform rules.</p>
                      <h3>7. Reservations and Collection</h3>
                      <p>A reservation is created when a consumer successfully reserves an available bundle through the platform.</p>
                      <p>Once a reservation is confirmed:</p>
                      <ul>
                        <li>The available quantity of that bundle may be reduced</li>
                        <li>A claim code may be generated for collection</li>
                        <li>The reservation remains subject to the listed pickup window</li>
                        <li>The seller may require a valid claim code before marking the bundle as collected</li>
                      </ul>
                      <p>A reservation does not guarantee indefinite availability. If a bundle is not collected in time, it may expire or be treated as a no-show in accordance with the platform’s lifecycle rules.</p>
                      <h3>8. Listings, Availability, and Accuracy</h3>
                      <p>Sellers are responsible for ensuring listings are as accurate as possible. This includes:</p>
                      <ul>
                        <li>Bundle contents or description</li>
                        <li>Allergens</li>
                        <li>Category</li>
                        <li>Declared weight</li>
                        <li>Collection time information</li>
                        <li>Price and quantity</li>
                      </ul>
                      <p>Although the platform includes validation and reservation controls, it does not guarantee that every listing is error-free, complete, or continuously available.</p>
                      <h3>9. Food Safety and Allergens</h3>
                      <p>Food bundles listed through the platform may contain allergens or may have been handled in environments where cross-contamination is possible.</p>
                      <p>Consumers are responsible for checking all available listing information before reserving or consuming any bundle.</p>
                      <p>While sellers are expected to provide accurate allergen information, tlll.com cannot guarantee that bundle information is complete, fully up to date, or suitable for every dietary requirement or medical condition.</p>
                      <p>All food collected through the platform is accepted and consumed at the consumer’s own risk.</p>
                      <h3>10. Issue Reporting</h3>
                      <p>The platform may provide issue reporting tools that allow users to flag problems such as:</p>
                      <ul>
                        <li>Unavailable bundles</li>
                        <li>Inaccurate listings</li>
                        <li>Collection disputes</li>
                        <li>Quality concerns</li>
                        <li>Inappropriate platform use</li>
                      </ul>
                      <p>Submitting a report does not automatically entitle a user to compensation, replacement, or any specific outcome. Maintainers and, where relevant, sellers may review reports and take action at their discretion under platform policy.</p>
                      <p>False, abusive, or malicious reports may result in account restrictions.</p>
                      <h3>11. Badges, Streaks, and Analytics</h3>
                      <p>The platform may include user engagement and analytics features such as:</p>
                      <ul>
                        <li>Streak tracking</li>
                        <li>Badges</li>
                        <li>Impact summaries</li>
                        <li>Seller analytics</li>
                        <li>Forecasting outpits</li>
                      </ul>
                      <p>These features are informational or motivational in nature. They do not create contractual rights, financial guarantees, or entitlements. Forecasts, impact summaries, and similar metrics are estimates only and should not be relied upon as guarantees of future performance.</p>
                      <h3>12. Acceptable Use</h3>
                      <p>You must not:</p>
                      <ul>
                        <li>Misuse the reservation process</li>
                        <li>Submit false listings or false reports</li>
                        <li>Attempt to bypass stock or role restrictions</li>
                        <li>Scrape, copy, or interfere with platform data or operation</li>
                        <li>Upload unlawful, offensive, or deceptive content</li>
                        <li>Attempt to exploit system vulnerabilities, security flaws, or prototype limitations</li>
                      </ul>
                      <h3>13. Prototype and Educational Use</h3>
                      <p>tlll.com is an educational prototype developed as part of a university software project.</p>
                      <p>As a result:</p>
                      <ul>
                        <li>Some features may be incomplete, experimental, or subject to change</li>
                        <li>Service availability is not guaranteed</li>
                        <li>Data may be seeded, simulated, or used for demonstration and evaluation purposes</li>
                        <li>Bugs, interruptions, and feature revisions may occur</li>
                      </ul>
                      <p>The platform is provided on an “as available” basis for educational and demonstration purposes.</p>
                      <h3>14. Privacy and Data Use</h3>
                      <p>The platform stores limited account, listing, reservation, and operational data in order to provide its core functionality.</p>
                      <p>This may include:</p>
                      <ul>
                        <li>User role information</li>
                        <li>Display names or seller details</li>
                        <li>Bundle listing information</li>
                        <li>Reservation records</li>
                        <li>Claim-code and status information</li>
                        <li>Issue report data</li>
                        <li>Forecasting or analytics data linked to platform activity</li>
                      </ul>
                      <p>Data is used only for platform operation, testing, evaluation, improvement, and administration in line with the project’s educational purpose.</p>
                      <h3>15. Intellectual Property</h3>
                      <p>Unless otherwise stated, the platform’s source code, branding, layout, written content, and associated design materials belong to the project team or are used with permission.</p>
                      <p>Users must not reproduce, distribute, reverse engineer, or commercially exploit platform materials without permission, except where permitted by law.</p>
                      <h3>16. Limitation of Liability</h3>
                      <p>To the fullest extent permitted by law, tlll.com and its developers are not liable for:</p>
                      <ul>
                        <li>Inaccurate or incomplete seller listings</li>
                        <li>Missed collections, expired reservations, or no-show outcomes</li>
                        <li>Allergen, dietary, freshness, or food-safety issues</li>
                        <li>Temporary unavailability of the service</li>
                        <li>Prototype bugs, errors, or interruptions</li>
                        <li>Indirect or consequential losses arising from use of the platform</li>
                      </ul>
                      <p>Nothing in these Terms excludes liability that cannot legally be excluded.</p>
                      <h3>17. Suspension or Termination</h3>
                      <p>We may suspend, restrict, or terminate access where a user:</p>
                      <ul>
                        <li>Breaches these Terms</li>
                        <li>Misuses the platform</li>
                        <li>Creates risk for other users</li>
                        <li>Attempts unauthorised access</li>
                        <li>Repeatedly makes false reservations or reports</li>
                        <li>Undermines the safe or fair operation of the service</li>
                      </ul>
                      <h3>18. Changes to the Terms</h3>
                      <p>These Terms may be updated as the platform develops. Continued use of the platform after revised Terms are published constitutes acceptance of those changes.</p>
                      <h3>19. Contact</h3>
                      <p>For questions about these Terms, please contact:</p>
                      <p>gtgs201@exeter.ac.uk</p>
                    </div>
                    <button onClick={() => setConditions(false)}>Close</button>
                    </div>
                  )}
                  <div className="rowRegister">
                    <button onClick={createAccount} //was close popup
                              disabled={password!==confirmPassword || !timeValidForSeller || invalidTime || !validPassword || !agree}
                              >Create Account</button>
                    <button onClick={handleCancel}>Cancel</button>
                  </div>
                </div>
              )}
      </div>
      </div>
    </div>
  );
}

//exports the component so it can be imported in other files
export default LoginPage;

import { Navigate } from "react-router-dom";

function ProtectedRoute({ user, requireRole, children }) {
  

  
   if (!user) return <Navigate to="/login" replace />; //If the user has no login, redirect to the login page
    
  

  
  if (requireRole && user.role !== requireRole) { //If the user is logged in but doesn't have correct role permissions, direct to unauthorised page
    return <Navigate to="/unauthorised" replace />;
  }

 
  return children; //Otherwise, allow the user to access desired page if authorised
}

export default ProtectedRoute; //exports the component so it can be imported in other files


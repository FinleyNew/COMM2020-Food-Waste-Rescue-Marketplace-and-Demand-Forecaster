import { Navigate } from "react-router-dom";

function ProtectedRoute({ user, requireRole, children }) {
  

    
   if (!user) return <Navigate to="/login" replace />;
    
  

  
  if (requireRole && user.role !== requireRole) {
    return <Navigate to="/unauthorised" replace />;
  }

 
  return children;
}

export default ProtectedRoute;


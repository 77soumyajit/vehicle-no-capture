import { Navigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";

function ProtectedRoute({ children }) {

    const { user, loading } = useAuth();

    if (loading) {

        return <h3 className="text-center mt-5">Loading...</h3>;

    }

    if (!user) {

        return <Navigate to="/login" replace />;

    }

    return children;

}

export default ProtectedRoute;
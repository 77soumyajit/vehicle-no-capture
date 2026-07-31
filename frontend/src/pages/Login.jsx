import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { loginUser, getCurrentUser } from "../api/authApi";
import { useAuth } from "../hooks/useAuth";

import "../styles/login.css";

function Login() {
    const navigate = useNavigate();

    const { login } = useAuth();

    const [form, setForm] = useState({
        username: "",
        password: "",
    });

    const [loading, setLoading] = useState(false);

    const [showPassword, setShowPassword] = useState(false);

    const [error, setError] = useState("");

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        setLoading(true);

        setError("");

        try {
            const response = await loginUser(form);

            localStorage.setItem(
                "access_token",
                response.access_token
            );

            localStorage.setItem(
                "refresh_token",
                response.refresh_token
            );

            const currentUser = await getCurrentUser();

            login(currentUser);

            navigate("/");
        } catch (err) {
            setError(
                err.response?.data?.detail ||
                "Login failed."
            );
        }

        setLoading(false);
    };

    return (
        <div className="login-page">

            <div className="login-left">

                <div>

                    <h1>🚗 Vehicle Gate Pass</h1>

                    <h2>AI Powered Vehicle Management</h2>

                    <p>
                        Secure Login
                    </p>

                </div>

            </div>

            <div className="login-right">

                <div className="login-card">

                    <h3 className="mb-4">
                        Sign In
                    </h3>

                    {error && (
                        <div className="alert alert-danger">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit}>

                        <div className="mb-3">

                            <label>
                                Username
                            </label>

                            <input
                                className="form-control"
                                name="username"
                                value={form.username}
                                onChange={handleChange}
                                required
                            />

                        </div>

                        <div className="mb-4">

                            <label>
                                Password
                            </label>

                            <input
                                type={
                                    showPassword
                                        ? "text"
                                        : "password"
                                }
                                className="form-control"
                                name="password"
                                value={form.password}
                                onChange={handleChange}
                                required
                            />

                            <div className="form-check mt-2">

                                <input
                                    className="form-check-input"
                                    type="checkbox"
                                    onChange={() =>
                                        setShowPassword(
                                            !showPassword
                                        )
                                    }
                                />

                                <label className="form-check-label">
                                    Show Password
                                </label>

                            </div>

                        </div>

                        <button
                            className="btn btn-primary w-100"
                            disabled={loading}
                        >

                            {loading
                                ? "Signing In..."
                                : "Login"}

                        </button>

                    </form>

                </div>

            </div>

        </div>
    );
}

export default Login;
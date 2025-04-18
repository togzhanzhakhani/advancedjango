import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import '../css/auth.css'

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post("http://localhost:8000/api/token/", {
        username: username,
        password: password,
      });
      const { access, refresh, role } = response.data;
      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);
      localStorage.setItem("role", role);
      console.log("Login successful:", response.data);
      navigate("/");
    } catch (error) {
      console.error("Error during login:", error);
    }
  };

  return (
    <div className="login-container">
      <h2 className="login-title">Login</h2>
      <form onSubmit={handleLogin} className="login-form">
        <div className="form-group">
          <label className="label">Username:</label>
          <input
            type="text"
            className="input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter your username"
          />
        </div>
        <div className="form-group">
          <label className="label">Password:</label>
          <input
            type="password"
            className="input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
          />
        </div>
        <button type="submit" className="submit-button">Login</button>
      </form>
      <div className="login-link">
        <p>Don't have an account?</p>
        <button onClick={() => navigate("/register")} className="link-button">Register Here</button>
      </div>
      <div className="login-link">
        <p>Forgot your password?</p>
        <button onClick={() => navigate("/reset-password")} className="link-button">Reset Password</button>
      </div>
    </div>
  );
}

export default Login;

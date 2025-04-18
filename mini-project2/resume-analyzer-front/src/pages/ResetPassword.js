import React, { useState } from "react";
import axios from "axios";
import '../css/resetpass.css'

function ResetPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleResetPassword = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post("http://localhost:8000/api/password_reset/", {
        email: email,
      });
      setMessage("Password reset link has been sent to your email!");
    } catch (error) {
      setMessage("Error during password reset. Please try again.");
      console.error("Error during password reset:", error);
    }
  };

  return (
    <div className="reset-password-container">
      <h2 className="reset-password-title">Reset Password</h2>
      <form onSubmit={handleResetPassword} className="reset-password-form">
        <div className="form-group">
          <label className="label">Email:</label>
          <input
            type="email"
            className="input"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
          />
        </div>
        <button type="submit" className="submit-button">Send Reset Link</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default ResetPassword;

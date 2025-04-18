import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ResumeUpload from "./ResumeUpload"; 
import ResumeList from "./ResumeList";
import '../css/auth.css'

const Home = () => {
  const [userRole, setUserRole] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const role = localStorage.getItem("role");
    if (!role) {
      navigate("/login"); 
    } else {
      setUserRole(role);
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("role");
    navigate("/login");
  };

  return (
    <div>
      <button onClick={handleLogout} className="logout-button">Logout</button>
      {userRole === "job_seeker" ? (
        <ResumeUpload />
      ) : userRole === "recruiter" ? (
        <ResumeList />
      ) : (
        <p>Invalid role</p>
      )}
    </div>
  );
};

export default Home;

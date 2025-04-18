import React, { useEffect, useState } from "react";
import axios from "axios";
import '../css/resumes.css'
import { useNavigate } from 'react-router-dom'; 

const ResumeList = () => {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      navigate("/login");
    } else {
        const fetchResumes = async () => {
        try {
            const response = await axios.get("http://localhost:8000/api/resumes/");
            setResumes(response.data);
            setLoading(false);
        } catch (error) {
            console.error("Error fetching resumes", error);
        }
        };
        fetchResumes();
    }
    }, [navigate]);

  if (loading) return <p>Loading...</p>;

  return (
    <div className="resume-list-container">
      <h2 className="resume-list-title">All Resumes</h2>
      <div className="resume-list">
        {resumes.map((resume) => (
          <div key={resume.id} className="resume-item">
            <h3>{resume.user}</h3>
            <p><strong>Specialization:</strong> {resume.specialization}</p>
            <a href={`http://localhost:8000${resume.file}`} target="_blank" rel="noopener noreferrer">View Resume</a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResumeList;

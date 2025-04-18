import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom'; 
import '../css/resume.css'

const ResumeUpload = () => {
  const [specializations, setSpecializations] = useState([]);
  const [selectedSpecialization, setSelectedSpecialization] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      navigate("/login");
    } else {
      axios.get('http://localhost:8000/api/specializations/')
        .then(response => {
          setSpecializations(response.data);
        })
        .catch(error => {
          console.error("Error fetching specializations", error);
        });
    }
  }, [navigate]);

  const handleDrop = (acceptedFiles) => {
    setResumeFile(acceptedFiles[0]);
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop: handleDrop,
    accept: '.pdf, .docx'
  });

  const handleSubmit = async (event) => {
    event.preventDefault();
    const token = localStorage.getItem("access_token");
    if (!token) {
      navigate("/login");
      return;
    }
    const formData = new FormData();
    formData.append("specialization", selectedSpecialization);
    formData.append("file", resumeFile);
    try {
      const response = await axios.post("http://localhost:8000/api/upload_resume/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          "Authorization": `Bearer ${token}` 
        }
      });
      setAnalysisResult(response.data.data);
    } catch (error) {
      if (error.response && error.response.status === 401) {
        try {
          const refreshToken = localStorage.getItem("refresh_token"); 
          const refreshResponse = await axios.post("http://localhost:8000/api/token/refresh/", {
            refresh: refreshToken 
          });
          const newAccessToken = refreshResponse.data.access;
          const newRefreshToken = refreshResponse.data.refresh;
          localStorage.setItem("access_token", newAccessToken);
          localStorage.setItem("refresh_token", newRefreshToken);
          const retryResponse = await axios.post("http://localhost:8000/api/upload_resume/", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
              "Authorization": `Bearer ${newAccessToken}`, 
            }
          });
          setAnalysisResult(retryResponse.data.data);
        } catch (refreshError) {
          console.error("Error refreshing token", refreshError);
          navigate("/login");
        }
      } else {
        console.error("Error uploading resume", error);
      }
    }
  };

  return (
    <div className="resume-upload-container">
      <h1 className="title">Upload Resume</h1>
      <form className="upload-form" onSubmit={handleSubmit}>
        <label className="form-label">
          Select Specialization:
          <select
            className="specialization-select"
            value={selectedSpecialization}
            onChange={(e) => setSelectedSpecialization(e.target.value)}
          >
            <option value="">Select Specialization</option>
            {specializations.map((specialization) => (
              <option key={specialization.id} value={specialization.id}>
                {specialization.name}
              </option>
            ))}
          </select>
        </label>
        <br />
        <div {...getRootProps()} className="dropzone">
          <input {...getInputProps()} />
          <p className="dropzone-text">Drag and drop your resume here, or click to select file (.pdf or .docx)</p>
          {resumeFile && <p>Selected file: {resumeFile.name}</p>}
        </div>
        <br />
        <button type="submit" className="submit-btn">Upload</button>
      </form>
  
      {analysisResult && (
        <div className="analysis-results">
          <h2 className="results-title">Analysis Result</h2>
          <p className="match-percentage">Skills Match: {analysisResult.skill_match_percentage}%</p>
  
          <h3 className="section-title">Matched Skills:</h3>
          {analysisResult.matched_skills && analysisResult.matched_skills.length > 0 ? (
            <ul className="skill-list">
              {analysisResult.matched_skills.map((skill) => (
                <li key={skill} className="skill-item">{skill}</li>
              ))}
            </ul>
          ) : (
            <p className="no-skills-message">No matched skills.</p>
          )}
  
          <h3 className="section-title">Missing Skills:</h3>
          {analysisResult.missing_skills && analysisResult.missing_skills.length > 0 ? (
            <ul className="skill-list">
              {analysisResult.missing_skills.map((skill) => (
                <li key={skill} className="skill-item">{skill}</li>
              ))}
            </ul>
          ) : (
            <p className="no-skills-message">No missing skills.</p>
          )}
  
          <h3 className="section-title">Resume Improvement Suggestions:</h3>
          <ul className="suggestions-list">
            {analysisResult.resume_improvement_suggestions.map((suggestion, index) => (
              <li key={index} className="suggestion-item">{suggestion}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );  
};

export default ResumeUpload;
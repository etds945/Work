import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ProjectDashboard.css'; // Corrected path

const ProjectList = () => {
    const [projects, setProjects] = useState([]);

    useEffect(() => {
        const API_URL = process.env.REACT_APP_API_URL;
        axios.get(`${API_URL}/projects`)
            .then(response => setProjects(response.data))
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    return (
        <div className="project-list">
            <h1>Project Quality Dashboard</h1>
            <ul>
                {projects.map(project => (
                    <li key={project.id}>
                        {project.name} - Quality Score: {project.qualityScore}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ProjectList;

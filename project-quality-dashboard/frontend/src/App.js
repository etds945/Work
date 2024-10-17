// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import './components/ProjectDashboard.css';
import ProjectList from './components/ProjectList';
import NewProjectForm from './components/NewProjectForm';
import axios from 'axios';

function App() {
    const [projects, setProjects] = useState([]);
    const [error, setError] = useState('');

    // Function to fetch projects from the backend
    const fetchProjects = async () => {
        const API_URL = process.env.REACT_APP_API_URL;
        try {
            const response = await axios.get(`${API_URL}/projects`);
            setProjects(response.data);
        } catch (error) {
            console.error('Error fetching projects:', error);
            setError('Failed to load projects. Please try again later.');
        }
    };

    // Fetch projects on component mount
    useEffect(() => {
        fetchProjects();
    }, []);

    // Function to handle adding a new project
    const handleProjectAdded = (newProject) => {
        setProjects([...projects, newProject]); // Update project list with new project
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>Project Quality Dashboard</h1>
                <NewProjectForm onProjectAdded={handleProjectAdded} />
                {error && <p className="error-message">{error}</p>}
                <ProjectList projects={projects} />
            </header>
        </div>
    );
}

export default App;

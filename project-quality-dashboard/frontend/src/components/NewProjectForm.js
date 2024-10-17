import React, { useState } from 'react';
import axios from 'axios';
import './ProjectDashboard.css';

const NewProjectForm = ({ onProjectAdded }) => {
    const [name, setName] = useState('');
    const [status, setStatus] = useState('ongoing');
    const [qualityScore, setQualityScore] = useState(100);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const project = { name, status, qualityScore };
        const API_URL = process.env.REACT_APP_API_URL;

        // Input validation: Ensure qualityScore is <= 100
        if (qualityScore > 100) {
            setError('Quality Score cannot exceed 100.');
            return;
        }

        try {
            const response = await axios.post(`${API_URL}/projects`, project);
            onProjectAdded(response.data); // Update the project list in App component
            setName('');
            setStatus('ongoing');
            setQualityScore(100);
            setError('');
        } catch (error) {
            console.error('Error creating project:', error);
            if (error.response && error.response.data && error.response.data.error) {
                setError(error.response.data.error);
            } else {
                setError('Failed to create project. Please try again.');
            }
        }
    };

    return (
        <form onSubmit={handleSubmit} className="new-project-form">
            {error && <p className="error-message">{error}</p>}
            <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Project Name"
                required
            />
            <select value={status} onChange={(e) => setStatus(e.target.value)}>
                <option value="ongoing">Ongoing</option>
                <option value="completed">Completed</option>
                <option value="in progress">In Progress</option>
            </select>
            <input
                type="number"
                value={qualityScore}
                onChange={(e) => setQualityScore(Number(e.target.value))}
                placeholder="Quality Score"
                required
                max={100} // HTML5 validation
            />
            <button type="submit">Add Project</button>
        </form>
    );
};

export default NewProjectForm;

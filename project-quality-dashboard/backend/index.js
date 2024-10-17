const express = require('express');
const cors = require('cors');
const app = express();
const sequelize = require('./config/database'); // Sequelize config
const Project = require('./models/Project');
const dotenv = require('dotenv');

dotenv.config(); // Load environment variables first

app.use(express.json()); // To handle JSON payload

// Configure CORS to allow requests from the frontend
app.use(cors({
    origin: 'https://congenial-dollop-r4ppjvr7p69qhxjjv-3001.app.github.dev', // Replace with your frontend's URL
    methods: ['GET', 'POST'],
    credentials: true,
}));

// Simple route to test
app.get('/', (req, res) => {
    res.send('Backend running successfully!');
});

// Route to fetch all projects
app.get('/projects', async (req, res) => {
    try {
        const projects = await Project.findAll();
        res.json(projects);
    } catch (err) {
        console.error('Error retrieving projects:', err);
        res.status(500).json({ error: 'Failed to retrieve projects' });
    }
});

// Route to create a new project
app.post('/projects', async (req, res) => {
    const { name, status, qualityScore } = req.body;

    try {
        const newProject = await Project.create({ name, status, qualityScore });
        res.status(201).json(newProject);
    } catch (err) {
        console.error('Error creating project:', err);
        if (err.name === 'SequelizeValidationError') {
            const messages = err.errors.map(e => e.message);
            res.status(400).json({ error: messages.join(', ') });
        } else {
            res.status(500).json({ error: 'Failed to create project' });
        }
    }
});

// Connect to the database and sync models, then start server
const PORT = process.env.PORT || 3000;

sequelize.authenticate()
    .then(() => {
        console.log('Connected to the database');
        return sequelize.sync({ force: true }); // Consider removing { force: true } in production
    })
    .then(() => {
        console.log('Database & tables created!');
        app.listen(PORT, () => {
            console.log(`Server running on port ${PORT}`);
        });
    })
    .catch(err => {
        console.error('Error connecting to the database:', err);
    });

// backend/models/Project.js
const { Sequelize, DataTypes } = require('sequelize');
const sequelize = require('../config/database'); // Sequelize instance

const Project = sequelize.define('Project', {
    name: {
        type: DataTypes.STRING,
        allowNull: false,
        validate: {
            notEmpty: true,
        },
    },
    status: {
        type: DataTypes.STRING,
        defaultValue: 'ongoing',
        validate: {
            isIn: [['ongoing', 'completed', 'in progress']],
        },
    },
    qualityScore: {
        type: DataTypes.INTEGER,
        defaultValue: 100,
        validate: {
            min: 0,
            max: 100,
        },
    },
}, {
    timestamps: true, // Ensure `createdAt` and `updatedAt` fields are auto-populated
});

module.exports = Project;

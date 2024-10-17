const { Sequelize } = require('sequelize');
const dotenv = require('dotenv');

dotenv.config(); // Load environment variables first

// Initialize Sequelize to connect to the MySQL database
const sequelize = new Sequelize(
    process.env.DB_NAME,
    process.env.DB_USER,
    process.env.DB_PASSWORD,
    {
        host: process.env.DB_HOST,
        dialect: 'mysql',
        logging: false, // Optional: Disable SQL query logging
    }
);

console.log('Sequelize Config:', {
    database: process.env.DB_NAME,
    username: process.env.DB_USER,
    password: process.env.DB_PASSWORD ? '***' : 'NO PASSWORD',
    host: process.env.DB_HOST,
    dialect: 'mysql',
});

module.exports = sequelize;

# frontend/Dockerfile

# Use an official Node.js runtime as the base image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install all dependencies
RUN npm install

# Copy the .env file
COPY .env ./

# Copy the rest of the application code to the container
COPY . .

# Expose the port your application runs on
EXPOSE 3000

# Start the React app
CMD ["npm", "start"]

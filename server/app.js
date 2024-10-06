const tf = require('@tensorflow/tfjs-node'); // TensorFlow.js for Node.js
const express = require('express'); // For creating the web server
const fs = require('fs');

// Initialize the express app
const app = express();
app.use(express.json());

// Load the model
let model;
async function loadModel() {
    try {
        model = await tf.loadLayersModel('file://model/model.json');
        console.log('Model loaded successfully');
    } catch (error) {
        console.error('Error loading the model:', error);
    }
}

// Predict function
async function makePrediction(inputData) {
    try {
        const inputTensor = tf.tensor2d([inputData]);
        const prediction = model.predict(inputTensor);
        return prediction.dataSync()[0]; // Return the prediction
    } catch (error) {
        console.error('Error making prediction:', error);
    }
}

// Endpoint to make a prediction
app.post('/predict', async (req, res) => {
    try {
        const inputData = req.body.inputData;

        // Log the input data
        console.log('Input data received:', inputData);

        // Ensure the input is shaped correctly for your model
        const inputTensor = tf.tensor2d([inputData], [1, 10]); // Shape must match the model input

        const prediction = model.predict(inputTensor);
        const predictionValue = prediction.dataSync()[0];

        // Log the prediction value
        console.log('Prediction value:', predictionValue);

        res.json({ prediction: predictionValue });
    } catch (error) {
        console.error('Error making prediction:', error);
        res.status(500).send('Error making prediction');
    }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, async () => {
    console.log(`Server is running on port ${PORT}`);
    await loadModel(); // Load the model when the server starts
});

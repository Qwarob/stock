const tf = require('@tensorflow/tfjs-node'); // Use '@tensorflow/tfjs' if running in the browser
const fs = require('fs');
const csv = require('csv-parser');

const dataPath = 'data/historical_data.csv'; // Path to your historical data

// Load your historical data
async function loadData() {
    return new Promise((resolve, reject) => {
        const data = { inputs: [], outputs: [] };
        
        fs.createReadStream(dataPath)
            .pipe(csv())
            .on('data', (row) => {
                const input = [
                    Number(row['Open']),
                    Number(row['High']),
                    Number(row['Low']),
                    Number(row['Close']),
                    Number(row['Volume']),
                    Number(row['Prev Close']),
                    Number(row['Avg Price']),
                    Number(row['Price Change %']),
                    Number(row['5-MA']),
                    Number(row['10-MA']),
                ]; // Extract features as input
                const output = Number(row['Close']); // Using close price as the output

                if (input.length === 10) {  // Ensure we have 10 features
                    data.inputs.push(input);
                    data.outputs.push(output);
                }
            })
            .on('end', () => {
                resolve(data);
            })
            .on('error', (error) => {
                reject(error);
            });
    });
}

async function trainModel(model, trainingData) {
    const xs = tf.tensor2d(trainingData.inputs, [trainingData.inputs.length, 10]); // Shape: [number of examples, 10]
    const ys = tf.tensor2d(trainingData.outputs, [trainingData.outputs.length, 1]); // Shape: [number of examples, 1]

    // Increase epochs for longer training and suppress logging
    await model.fit(xs, ys, { epochs: 200, verbose: 0 }); // Train for 200 epochs with no output
}

async function saveModel(model) {
    await model.save('file://model'); // Save locally
}

async function createModel() {
    const model = tf.sequential();
    model.add(tf.layers.dense({ inputShape: [10], units: 64, activation: 'relu' }));
    model.add(tf.layers.dense({ units: 64, activation: 'relu' }));
    model.add(tf.layers.dense({ units: 32, activation: 'relu' }));
    model.add(tf.layers.dense({ units: 16, activation: 'relu' }));
    model.add(tf.layers.dense({ units: 1 })); // Output layer

    model.compile({ optimizer: 'adam', loss: 'meanSquaredError' });
    return model;
}

(async () => {
    const trainingData = await loadData(); // Load your data
    const model = await createModel();
    await trainModel(model, trainingData);
    await saveModel(model);
})();

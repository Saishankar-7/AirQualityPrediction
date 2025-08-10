import React, { useState } from 'react';
import { Container, Box } from '@mui/material';
import Header from './components/Header';
import PredictionForm from './components/PredictionForm';
import ResultDisplay from './components/ResultDisplay';
import { predictionAPI } from './api/predictionAPI';
import './App.css';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePredict = async (formData) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const predictionResult = await predictionAPI.predictAirQuality(formData);
      setResult(predictionResult);
    } catch (err) {
      setError(err.message || 'An error occurred while making the prediction');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <Header />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <PredictionForm 
            onPredict={handlePredict} 
            loading={loading} 
            error={error} 
          />
          <ResultDisplay result={result} />
        </Box>
      </Container>
    </div>
  );
}

export default App;

import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Grid,
  Alert,
  CircularProgress,
} from '@mui/material';
import { styled } from '@mui/material/styles';

const StyledCard = styled(Card)(({ theme }) => ({
  maxWidth: 600,
  margin: 'auto',
  marginTop: theme.spacing(3),
}));

const PredictionForm = ({ onPredict, loading, error }) => {
  const [formData, setFormData] = useState({
    pm25: '',
    pm10: '',
    so2: '',
    no2: '',
    co: '',
    o3: '',
    temperature: '',
    humidity: '',
    wind_speed: '',
    pressure: '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Convert string inputs to numbers
    const numericData = {};
    Object.keys(formData).forEach(key => {
      numericData[key] = parseFloat(formData[key]) || 0;
    });
    
    onPredict(numericData);
  };

  const handleClear = () => {
    setFormData({
      pm25: '',
      pm10: '',
      so2: '',
      no2: '',
      co: '',
      o3: '',
      temperature: '',
      humidity: '',
      wind_speed: '',
      pressure: '',
    });
  };

  return (
    <StyledCard>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Enter Air Quality Parameters
        </Typography>
        
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        
        <Box component="form" onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="PM2.5 (μg/m³)"
                name="pm25"
                type="number"
                value={formData.pm25}
                onChange={handleChange}
                required
                inputProps={{ min: 0, step: 0.1 }}
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="PM10 (μg/m³)"
                name="pm10"
                type="number"
                value={formData.pm10}
                onChange={handleChange}
                required
                inputProps={{ min: 0, step: 0.1 }}
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="SO2 (μg/m³)"
                name="so2"
                type="number"
                value={formData.so2}
                onChange={handleChange}
                required
                inputProps={{ min: 0, step: 0.1 }}
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="NO2 (μg/m³)"
                name="no2"
                type="number"
                value={formData.no2}
                onChange={handleChange}
                required
                inputProps={{ min: 0, step: 0.1 }}
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="CO (mg/m³)"
                name="co"
                type="number"
                value={formData.co}
                onChange={handleChange}
                required
                inputProps={{ min: 0, step: 0.01 }}
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="O3 (μg/m³)"
                name="o3"
                type="number"
                value={formData.o3}
                onChange={handleChange}
                required
                inputProps={{ min: 0, step: 0.1 }}
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Temperature (°C)"
                name="temperature"
                type="number"
                value={formData.temperature}
                onChange={handleChange}
                required
                inputProps={{ step: 0.1 }}
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Humidity (%)"
                name="humidity"
                type="number"
                value={formData.humidity}
                onChange={handleChange}
                required
                inputProps={{ min: 0, max: 100, step: 0.1 }}
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Wind Speed (m/s)"
                name="wind_speed"
                type="number"
                value={formData.wind_speed}
                onChange={handleChange}
                required
                inputProps={{ min: 0, step: 0.1 }}
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Pressure (hPa)"
                name="pressure"
                type="number"
                value={formData.pressure}
                onChange={handleChange}
                required
                inputProps={{ min: 0, step: 0.1 }}
              />
            </Grid>
            
            <Grid item xs={12}>
              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
                <Button
                  type="submit"
                  variant="contained"
                  disabled={loading}
                  size="large"
                >
                  {loading ? <CircularProgress size={24} /> : 'Predict Air Quality'}
                </Button>
                
                <Button
                  type="button"
                  variant="outlined"
                  onClick={handleClear}
                  disabled={loading}
                  size="large"
                >
                  Clear
                </Button>
              </Box>
            </Grid>
          </Grid>
        </Box>
      </CardContent>
    </StyledCard>
  );
};

export default PredictionForm;

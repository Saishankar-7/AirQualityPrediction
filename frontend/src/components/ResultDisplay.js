import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Grid,
  Paper,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const StyledCard = styled(Card)(({ theme }) => ({
  maxWidth: 600,
  margin: 'auto',
  marginTop: theme.spacing(3),
}));

const ResultDisplay = ({ result }) => {
  if (!result) return null;

  const getAQIColor = (aqi) => {
    if (aqi <= 50) return '#00e400';
    if (aqi <= 100) return '#ffff00';
    if (aqi <= 150) return '#ff7e00';
    if (aqi <= 200) return '#ff0000';
    if (aqi <= 300) return '#8f3f97';
    return '#7e0023';
  };

  const getAQILevel = (aqi) => {
    if (aqi <= 50) return 'Good';
    if (aqi <= 100) return 'Moderate';
    if (aqi <= 150) return 'Unhealthy for Sensitive Groups';
    if (aqi <= 200) return 'Unhealthy';
    if (aqi <= 300) return 'Very Unhealthy';
    return 'Hazardous';
  };

  const pollutantData = [
    { name: 'PM2.5', value: result.pm25, unit: 'μg/m³' },
    { name: 'PM10', value: result.pm10, unit: 'μg/m³' },
    { name: 'SO2', value: result.so2, unit: 'μg/m³' },
    { name: 'NO2', value: result.no2, unit: 'μg/m³' },
    { name: 'CO', value: result.co, unit: 'mg/m³' },
    { name: 'O3', value: result.o3, unit: 'μg/m³' },
  ];

  return (
    <StyledCard>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Air Quality Prediction Result
        </Typography>
        
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          <Typography variant="h2" sx={{ 
            fontSize: '3rem', 
            fontWeight: 'bold',
            color: result.color 
          }}>
            {Math.round(result.aqi)}
          </Typography>
          
          <Chip
            label={result.level}
            sx={{
              bgcolor: result.color,
              color: 'white',
              fontSize: '1.2rem',
              fontWeight: 'bold',
              mt: 1,
            }}
          />
        </Box>
        
        <Typography variant="h6" gutterBottom>
          Pollutant Levels
        </Typography>
        
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={pollutantData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip 
              formatter={(value, name, props) => [
                `${value} ${props.payload.unit}`,
                name
              ]}
            />
            <Bar dataKey="value" fill="#1976d2" />
          </BarChart>
        </ResponsiveContainer>
        
        <Grid container spacing={2} sx={{ mt: 2 }}>
          {pollutantData.map((item) => (
            <Grid item xs={12} sm={6} key={item.name}>
              <Paper elevation={2} sx={{ p: 2 }}>
                <Typography variant="body2" color="textSecondary">
                  {item.name}
                </Typography>
                <Typography variant="h6">
                  {item.value} {item.unit}
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
        
        <Box sx={{ mt: 3, p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
          <Typography variant="body2" color="textSecondary">
            <strong>AQI Guide:</strong>
          </Typography>
          <Typography variant="body2" sx={{ mt: 1 }}>
            • 0-50: Good - Air quality is satisfactory<br/>
            • 51-100: Moderate - Acceptable for most people<br/>
            • 101-150: Unhealthy for Sensitive Groups<br/>
            • 151-200: Unhealthy - Everyone may experience effects<br/>
            • 201-300: Very Unhealthy - Health alert<br/>
            • 301+: Hazardous - Emergency conditions
          </Typography>
        </Box>
      </CardContent>
    </StyledCard>
  );
};

export default ResultDisplay;

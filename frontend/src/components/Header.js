import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';
import AirIcon from '@mui/icons-material/Air';

const Header = () => {
  return (
    <AppBar position="static" sx={{ bgcolor: '#1976d2' }}>
      <Toolbar>
        <AirIcon sx={{ mr: 2 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Air Quality Predictor
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Header;

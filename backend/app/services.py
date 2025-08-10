import numpy as np
import tensorflow as tf
from typing import Dict, List
import pickle
import os
import logging

logger = logging.getLogger(__name__)

class AirQualityPredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.model_loaded = False
        self.load_model_and_scaler()
    
    def load_model_and_scaler(self):
        """Load the pre-trained LSTM model and scaler"""
        try:
            # Get the directory of the current file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.join(current_dir, '..', '..')
            assets_dir = os.path.join(current_dir, '..', 'assets')
            
            # Check multiple possible model file locations
            model_paths = [
                os.path.join(assets_dir, 'air_quality_lstm_model.h5'),
                os.path.join(project_root, 'saved_model.keras'),
                os.path.join(project_root, 'saved_model.h5'),
                os.path.join(current_dir, '..', 'saved_model.keras')
            ]
            
            scaler_paths = [
                os.path.join(assets_dir, 'scaler.pkl'),
                os.path.join(project_root, 'scaler.pkl'),
                os.path.join(current_dir, '..', 'scaler.pkl')
            ]
            
            model_path = None
            for path in model_paths:
                if os.path.exists(path):
                    model_path = path
                    break
            
            scaler_path = None
            for path in scaler_paths:
                if os.path.exists(path):
                    scaler_path = path
                    break
            
            if not model_path or not os.path.exists(model_path):
                logger.warning(f"Model file not found in any expected location")
                logger.info("Using mock prediction service for testing")
                self.model_loaded = False
                return
                
            if not scaler_path or not os.path.exists(scaler_path):
                logger.warning(f"Scaler file not found in any expected location")
                logger.info("Using mock prediction service for testing")
                self.model_loaded = False
                return
            
            # Load the model
            self.model = tf.keras.models.load_model(model_path)
            logger.info(f"LSTM model loaded successfully from {model_path}")
            
            # Load the scaler
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            logger.info(f"Scaler loaded successfully from {scaler_path}")
            
            self.model_loaded = True
            
        except Exception as e:
            logger.error(f"Error loading model or scaler: {str(e)}")
            logger.info("Using mock prediction service for testing")
            self.model_loaded = False
    
    def predict(self, features: List[float]) -> Dict:
        """Make prediction using the loaded model or mock service"""
        try:
            if not self.model_loaded:
                # Mock prediction for testing
                logger.info("Using mock prediction service")
                mock_aqi = float(np.mean(features) * 2 + np.random.normal(0, 10))
                mock_aqi = max(0, min(500, mock_aqi))  # Clamp between 0-500
                return {
                    'aqi': mock_aqi,
                    'features': features
                }
            
            # Convert to numpy array
            features_array = np.array(features).reshape(1, -1)
            
            # Scale the features
            features_scaled = self.scaler.transform(features_array)
            
            # Reshape for LSTM (samples, timesteps, features)
            features_reshaped = features_scaled.reshape(1, 1, features_scaled.shape[1])
            
            # Make prediction
            prediction = self.model.predict(features_reshaped)
            
            # Get AQI value
            aqi = float(prediction[0][0])
            
            # Ensure AQI is non-negative and reasonable
            aqi = max(0, min(500, aqi))
            
            return {
                'aqi': aqi,
                'features': features
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            # Return mock prediction as fallback
            mock_aqi = float(np.mean(features) * 2)
            mock_aqi = max(0, min(500, mock_aqi))
            return {
                'aqi': mock_aqi,
                'features': features
            }
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance (placeholder for future implementation)"""
        # This is a placeholder - actual implementation would depend on model
        features = [
            'pm25', 'pm10', 'so2', 'no2', 'co', 'o3',
            'temperature', 'humidity', 'wind_speed', 'pressure'
        ]
        
        # Simple equal importance for now
        importance = {feature: 0.1 for feature in features}
        
        return importance

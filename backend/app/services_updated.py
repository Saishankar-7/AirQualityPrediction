import numpy as np
import tensorflow as tf
from typing import Dict, List
import pickle
import os
import logging
from sklearn.preprocessing import StandardScaler
import warnings

# Suppress TensorFlow warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

logger = logging.getLogger(__name__)

class AirQualityPredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.model_loaded = False
        self.load_model_and_scaler()
    
    def load_model_and_scaler(self):
        """Load the pre-trained LSTM model and scaler with improved error handling"""
        try:
            # Get the directory of the current file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            assets_dir = os.path.join(current_dir, '..', 'assets')
            
            # Check for available model files
            model_files = [
                'air_quality_lstm_model.h5',
                'saved_model.keras',
                'model.h5',
                'lstm_model.h5'
            ]
            
            model_path = None
            for model_file in model_files:
                test_path = os.path.join(assets_dir, model_file)
                if os.path.exists(test_path):
                    model_path = test_path
                    logger.info(f"Found model file: {model_file}")
                    break
            
            if model_path is None:
                # Try to load from model_path.pkl
                model_path_pkl = os.path.join(current_dir, '..', '..', 'model_path.pkl')
                if os.path.exists(model_path_pkl):
                    with open(model_path_pkl, 'rb') as f:
                        model_path = pickle.load(f)
                    logger.info(f"Loaded model path from model_path.pkl: {model_path}")
                else:
                    # Fallback to saved_model.keras in root directory
                    root_model_path = os.path.join(current_dir, '..', '..', 'saved_model.keras')
                    if os.path.exists(root_model_path):
                        model_path = root_model_path
                        logger.info(f"Using root model: {root_model_path}")
                    else:
                        raise FileNotFoundError("No model file found")
            
            # Load the model
            self.model = tf.keras.models.load_model(model_path)
            self.model_loaded = True
            logger.info("Model loaded successfully")
            
            # Load the scaler
            scaler_path = os.path.join(assets_dir, 'scaler.pkl')
            if os.path.exists(scaler_path):
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                logger.info("Scaler loaded successfully")
            else:
                # Create a default scaler if file doesn't exist
                logger.warning("Scaler file not found, creating default scaler")
                self.scaler = self._create_default_scaler()
                
        except Exception as e:
            logger.error(f"Error loading model or scaler: {str(e)}")
            # Create a dummy model for testing purposes
            self._create_dummy_model()
            logger.warning("Using dummy model for testing")
    
    def _create_default_scaler(self):
        """Create a default scaler for 10 features"""
        scaler = StandardScaler()
        # Fit with dummy data for 10 features
        dummy_data = np.array([
            [35.0, 55.0, 15.0, 40.0, 1.0, 60.0, 25.0, 60.0, 10.0, 1013.0]
        ])
        scaler.fit(dummy_data)
        return scaler
    
    def _create_dummy_model(self):
        """Create a dummy model for testing when actual model is not available"""
        try:
            # Create a simple model structure
            model = tf.keras.Sequential([
                tf.keras.layers.Dense(10, activation='relu', input_shape=(10,)),
                tf.keras.layers.Dense(5, activation='relu'),
                tf.keras.layers.Dense(1, activation='linear')
            ])
            model.compile(optimizer='adam', loss='mse')
            self.model = model
            self.scaler = self._create_default_scaler()
            self.model_loaded = False
        except Exception as e:
            logger.error(f"Error creating dummy model: {str(e)}")
    
    def validate_features(self, features: List[float]) -> bool:
        """Validate input features"""
        if not isinstance(features, list):
            return False
        if len(features) != 10:
            logger.error(f"Expected 10 features, got {len(features)}")
            return False
        if not all(isinstance(x, (int, float)) for x in features):
            return False
        return True
    
    def predict(self, features: List[float]) -> Dict:
        """Make prediction using the loaded model with validation"""
        try:
            if not self.validate_features(features):
                raise ValueError("Invalid input features")
            
            # Convert features to numpy array
            features_array = np.array(features).reshape(1, -1)
            
            # Scale the features
            features_scaled = self.scaler.transform(features_array)
            
            # Reshape for LSTM (samples, timesteps, features)
            features_reshaped = features_scaled.reshape(1, 1, features_scaled.shape[1])
            
            # Make prediction
            prediction = self.model.predict(features_reshaped, verbose=0)
            
            # Get AQI value
            aqi = float(prediction[0][0])
            
            # Ensure AQI is non-negative and reasonable
            aqi = max(0, min(aqi, 500))
            
            return {
                'aqi': round(aqi, 2),
                'model_loaded': self.model_loaded,
                'features': features
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            # Return a safe fallback value
            return {
                'aqi': 50.0,
                'model_loaded': self.model_loaded,
                'error': str(e),
                'features': features
            }
    
    def get_aqi_level(self, aqi: float) -> Dict[str, str]:
        """Get AQI level and corresponding color"""
        if aqi <= 50:
            return {"level": "Good", "color": "#00e400", "description": "Air quality is satisfactory"}
        elif aqi <= 100:
            return {"level": "Moderate", "color": "#ffff00", "description": "Air quality is acceptable"}
        elif aqi <= 150:
            return {"level": "Unhealthy for Sensitive Groups", "color": "#ff7e00", "description": "Sensitive groups may experience health effects"}
        elif aqi <= 200:
            return {"level": "Unhealthy", "color": "#ff0000", "description": "Everyone may begin to experience health effects"}
        elif aqi <= 300:
            return {"level": "Very Unhealthy", "color": "#8f3f97", "description": "Health alert: everyone may experience more serious health effects"}
        else:
            return {"level": "Hazardous", "color": "#7e0023", "description": "Health warnings of emergency conditions"}
    
    def get_feature_names(self) -> List[str]:
        """Get the list of feature names"""
        return [
            'pm25', 'pm10', 'so2', 'no2', 'co', 'o3',
            'temperature', 'humidity', 'wind_speed', 'pressure'
        ]
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        return {
            'model_loaded': self.model_loaded,
            'feature_count': 10,
            'features': self.get_feature_names(),
            'output': 'AQI (Air Quality Index)',
            'model_type': 'LSTM' if self.model_loaded else 'Dummy'
        }
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance (placeholder for future implementation)"""
        features = self.get_feature_names()
        
        # Simple equal importance for now
        importance = {feature: round(1.0/len(features), 3) for feature in features}
        
        return importance
    
    def batch_predict(self, features_list: List[List[float]]) -> List[Dict]:
        """Make predictions for multiple sets of features"""
        results = []
        for features in features_list:
            result = self.predict(features)
            results.append(result)
        return results

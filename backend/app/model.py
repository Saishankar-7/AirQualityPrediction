import tensorflow as tf
import pickle
import os
import logging

logger = logging.getLogger(__name__)

class ModelLoader:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_model()
    
    def load_model(self):
        """Load the pre-trained LSTM model and scaler"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            assets_dir = os.path.join(current_dir, '..', 'assets')
            
            # Load model
            model_path = os.path.join(assets_dir, 'air_quality_lstm_model.h5')
            self.model = tf.keras.models.load_model(model_path)
            logger.info("Model loaded successfully")
            
            # Load scaler
            scaler_path = os.path.join(assets_dir, 'scaler.pkl')
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            logger.info("Scaler loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def get_model(self):
        """Return the loaded model"""
        return self.model
    
    def get_scaler(self):
        """Return the loaded scaler"""
        return self.scaler

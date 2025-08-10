# Air Quality Prediction System

A full-stack application for predicting air quality using LSTM neural networks. The system includes a FastAPI backend and React frontend for real-time air quality predictions.

## 🚀 Features

- **Real-time Air Quality Prediction** using LSTM neural networks
- **RESTful API** built with FastAPI
- **Interactive Frontend** built with React and Material-UI
- **Comprehensive Input Parameters** including PM2.5, PM10, SO2, NO2, CO, O3, temperature, humidity, wind speed, and pressure
- **AQI Classification** with color-coded results
- **Mock Prediction Service** for testing without model files
- **CORS Support** for seamless frontend-backend communication

## 📁 Project Structure

```
air-quality-prediction/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI application
│   │   ├── services.py      # Prediction service
│   │   ├── schemas.py       # Pydantic models
│   │   └── model.py         # Model utilities
│   ├── assets/              # Model files directory
│   ├── requirements.txt     # Python dependencies
│   └── .gitignore
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── api/             # API service
│   │   ├── App.js           # Main React app
│   │   └── index.js         # React entry point
│   ├── package.json         # Node.js dependencies
│   └── .gitignore
├── kaggle_data/             # Training data
└── README.md
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- pip (Python package manager)
- npm (Node package manager)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare model files (optional):**
   - Place your trained model files in `backend/assets/`:
     - `air_quality_lstm_model.h5` (LSTM model)
     - `scaler.pkl` (feature scaler)
   - If no model files are provided, the system will use mock predictions for testing

5. **Run the backend:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

The frontend will automatically open at `http://localhost:3000`

## 🔧 API Endpoints

### Health Check
- **GET** `/` - Root endpoint
- **GET** `/health` - Health check and model status

### Predictions
- **POST** `/predict` - Predict air quality
  ```json
  {
    "pm25": 25.5,
    "pm10": 45.2,
    "so2": 12.3,
    "no2": 35.7,
    "co": 0.8,
    "o3": 85.4,
    "temperature": 22.5,
    "humidity": 65.0,
    "wind_speed": 3.2,
    "pressure": 1013.25
  }
  ```
  **Response:**
  ```json
  {
    "aqi": 75.5,
    "level": "Moderate",
    "color": "#ffff00",
    "pm25": 25.5,
    "pm10": 45.2,
    "so2": 12.3,
    "no2": 35.7,
    "co": 0.8,
    "o3": 85.4
  }
  ```

- **GET** `/model-info` - Get model information

## 🧪 Testing

### Backend Testing
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test prediction endpoint
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"pm25": 25.5, "pm10": 45.2, "so2": 12.3, "no2": 35.7, "co": 0.8, "o3": 85.4, "temperature": 22.5, "humidity": 65.0, "wind_speed": 3.2, "pressure": 1013.25}'
```

### Frontend Testing
1. Open `http://localhost:3000`
2. Fill in the air quality parameters
3. Click "Predict Air Quality"
4. View the results with AQI and classification

## 🎯 Usage Guide

1. **Start both backend and frontend servers**
2. **Open the frontend** at `http://localhost:3000`
3. **Enter air quality parameters**:
   - PM2.5 and PM10 concentrations
   - Gas concentrations (SO2, NO2, CO, O3)
   - Weather parameters (temperature, humidity, wind speed, pressure)
4. **Click "Predict Air Quality"** to get results
5. **View the AQI** and air quality classification

## 🔍 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure backend is running on `http://localhost:8000`
2. **Model Loading**: Check that model files exist in `backend/assets/`
3. **Port Conflicts**: Change ports in backend/frontend configs if needed
4. **Dependencies**: Run `pip install -r requirements.txt` and `npm install`

### Mock Predictions
If no model files are provided, the system automatically uses mock predictions:
- AQI is calculated as: `mean(features) * 2 + random_noise`
- Results are clamped between 0-500 for realistic values

## 📊 AQI Categories

| AQI Range | Level | Color | Description |
|-----------|--------|--------|-------------|
| 0-50 | Good | #00e400 | Air quality is satisfactory |
| 51-100 | Moderate | #ffff00 | Air quality is acceptable |
| 101-150 | Unhealthy for Sensitive Groups | #ff7e00 | Sensitive individuals may experience health effects |
| 151-200 | Unhealthy | #ff0000 | Everyone may begin to experience health effects |
| 201-300 | Very Unhealthy | #8f3f97 | Health alert: everyone may experience more serious effects |
| 301-500 | Hazardous | #7e0023 | Health warnings of emergency conditions |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- FastAPI team for the excellent web framework
- TensorFlow team for the machine learning framework
- Material-UI team for the React components
- Kaggle community for air quality datasets

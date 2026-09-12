🏠 House Price Prediction API

A machine learning-based REST API that predicts house prices based on property features such as location, area, number of bedrooms, bathrooms, and other relevant attributes.

The project uses Python, Machine Learning, FastAPI, and Scikit-learn to train a prediction model and expose it through a REST API.

🚀 Features

- House price prediction using Machine Learning
- REST API built with FastAPI
- Input validation using Pydantic
- Trained ML model served through an API
- Automatic API documentation with Swagger UI
- Model prediction endpoint
- Easy local setup and testing

🛠️ Technologies Used

- Python
- FastAPI
- Scikit-learn
- Pandas
- NumPy
- Pydantic
- Uvicorn
- Joblib

📁 Project Structure

house-price-prediction-api/
│
├── app/
│   ├── main.py
│   ├── model.py
│   └── schemas.py
│
├── model/
│   ├── house_price_model.pkl
│   └── scaler.pkl
│
├── data/
│   └── house_data.csv
│
├── notebooks/
│   └── house_price_prediction.ipynb
│
├── requirements.txt
├── README.md
└── .gitignore

«Your actual folder structure can be different. Update this section if your project uses different file names.»

📊 Machine Learning Workflow

The project follows a typical machine learning pipeline:

Dataset
   ↓
Data Cleaning
   ↓
Exploratory Data Analysis
   ↓
Feature Engineering
   ↓
Train/Test Split
   ↓
Model Training
   ↓
Model Evaluation
   ↓
Save Model
   ↓
FastAPI
   ↓
Prediction API

⚙️ Installation

1. Clone the repository

git clone https://github.com/your-username/house-price-prediction-api.git
cd house-price-prediction-api

2. Create a virtual environment

python -m venv venv

3. Activate the virtual environment

Windows:

venv\Scripts\activate

Linux/macOS:

source venv/bin/activate

4. Install dependencies

pip install -r requirements.txt

▶️ Run the API

Start the FastAPI application using:

uvicorn app.main:app --reload

The API will run at:

http://127.0.0.1:8000

📚 API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI

Open:

http://127.0.0.1:8000/docs

ReDoc

Open:

http://127.0.0.1:8000/redoc

🔮 Prediction Endpoint

"POST /predict"

This endpoint accepts house/property information and returns the predicted house price.

Example Request

{
  "area": 1500,
  "bedrooms": 3,
  "bathrooms": 2,
  "location": "Noida",
  "parking": 1
}

Example Response

{
  "predicted_price": 8500000
}

«Update the request fields according to the features used by your trained model.»

🧠 Model Training

The model can be trained using the provided dataset/notebook.

Example:

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

The trained model can then be saved using Joblib:

import joblib

joblib.dump(model, "model/house_price_model.pkl")

📈 Model Evaluation

The model can be evaluated using regression metrics such as:

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score

Example:

from sklearn.metrics import mean_absolute_error, r2_score

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("MAE:", mae)
print("R² Score:", r2)

🧪 Testing

You can test the API using:

- Swagger UI
- Postman
- cURL
- Python requests

Example:

curl -X POST "http://127.0.0.1:8000/predict" \
-H "Content-Type: application/json" \
-d "{\"area\":1500,\"bedrooms\":3,\"bathrooms\":2,\"location\":\"Noida\",\"parking\":1}"

🔐 Environment Variables

If the project requires environment variables, create a ".env" file:

MODEL_PATH=model/house_price_model.pkl

Do not commit sensitive credentials or ".env" files to GitHub.

📦 Requirements

Example "requirements.txt":

fastapi
uvicorn
pandas
numpy
scikit-learn
joblib
pydantic
python-dotenv

🔄 Future Improvements

Possible improvements include:

- Add a frontend interface
- Deploy the API to a cloud platform
- Add authentication
- Add database integration
- Improve model accuracy
- Add automated model retraining
- Add Docker support
- Add CI/CD pipeline
- Add API unit and integration tests
- Add monitoring and logging

👨‍💻 Author

Your Name

GitHub: "https://github.com/your-username"

📄 License

This project is created for educational and demonstration purposes.

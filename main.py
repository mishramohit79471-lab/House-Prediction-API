import joblib
import pandas as pd
import io

from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, Field


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent

FRONTEND_DIR = BASE_DIR / "frontend"

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)

model = joblib.load(BASE_DIR / "house_model.joblib")
features = joblib.load(BASE_DIR / "house_features.joblib")

@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")

#input schema
class Housefeatures(BaseModel):
    MedInc : float = Field(gt=0, description="Median Income of Neighbourhood")
    HouseAge: float = Field(gt=0, description="average age house in the block")
    AveRooms: float = Field(gt=0, description="Average number of rooms per household")
    AveBedrms: float = Field(gt=0, description="Average number of bedrooms per household")
    Population: float = Field(gt=0, description="Block population")
    AveOccup: float = Field(gt=0, description="Average number of household members")
    Latitude: float = Field(ge=32, le=42, description="Latitude of the block")
    Longitude: float = Field(ge=-125, le=-114, description="Longitude of the block")


class PredictionResponse(BaseModel):
    predicted_price: float = Field(description="Predicted house value in hundreds of thousands of dollars")
    predicted_price_usd: float = Field(description="Predicted house value in US dollars")

#home
@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/health")
def health():
    return {
        "status":"running",
        "model":"RandomForestRegressor",
        "features":features,
        "avg_error":"$32,754"
    }

#prediction
@app.post("/predict", response_model=PredictionResponse)
def predict(house: Housefeatures):
    try:
        input_data = pd.DataFrame([house.model_dump()], columns=features)
        predicted = float(model.predict(input_data)[0])
        price_usd = predicted * 100000

        return {
            "predicted_price": predicted,
            "predicted_price_usd": price_usd,
        }
    except Exception as e:
        raise HTTPException(
            status_code =500,
            detail = f"prediction failed: {str(e)}"
        )


@app.post("/predict-file")
async def predict_file(file: UploadFile=File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="please upload a CSV File only"
        )

    contents = await file.read()

    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"could not read CSV file: {str(e)}"
        )

    required_columns = [
        "MedInc", "HouseAge", "AveRooms", "AveBedrms",
        "Population", "AveOccup", "Latitude", "Longitude"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=f"These columns are missing from your file: {missing_columns}"
        )

    if len(df) == 0:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file has no data rows"
        )

    try:
        prediction = model.predict(df[required_columns])
        df["predicted_price_usd"] = prediction * 100000
        df["predicted_price_usd"] = df["predicted_price_usd"].map(lambda x: f"${x:,.0f}")

        output = df.to_csv(index=False)

        return StreamingResponse(
            io.StringIO(output),
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=prediction.csv"
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"prediction failed: {str(e)}"
        )

        
from typing import Any, Dict
from sklearn_deploy import __version__
import pytest
import pickle
import numpy as np
import pandas as pd
from validation import PredictionData
from sklearn.pipeline import Pipeline

def test_version():
    assert __version__ == '0.1.0'

@pytest.fixture
def model() -> Any:
    """Load the model to be injected in tests"""
    with open("airbnb_regressor.pickle","rb") as f:
        model = pickle.load(f)
    return model

@pytest.fixture()
def raw_data() -> Dict:
    """Data as it will posted trough the API endpoint for prediction"""
    return {"neighbourhood":"Buttes-Montmartre","room_type":"Entire home/apt","minimum_nights":1.555,"mois":2,"voyageurs":2.5,"chambres":1,"lits":1,"salle_de_bains":1}

def test_init_prediction_data(raw_data):
    """Assert that the PredcitionData declared can init with the raw_data"""
    prediction_data = PredictionData(**raw_data)
    assert prediction_data

def test_is_pipeline(model):
    """Assert that the model load is of sklearn Pipeline type"""
    assert type(model) == Pipeline

def test_prediction(model, raw_data):
    """Assert that the model can predict the raw_data"""
    data = PredictionData(**raw_data)
    formated_data = {}
    for key, value in data.dict().items():
        formated_data[key] = [value]
    df = pd.DataFrame(formated_data)
    res = model.predict(df)[0]
    assert type(res) == np.float64
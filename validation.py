from pydantic import BaseModel


class PredictionData(BaseModel):
    neighbourhood: str
    room_type: str
    minimum_nights: float
    mois: int
    voyageurs: float
    chambres: float
    lits: float
    salle_de_bains: float

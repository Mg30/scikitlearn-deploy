from pydantic import BaseModel


class PredictionData(BaseModel):
    """ Validation class for FastApi
     Attributs must match:
     1- names of the columns of trained data
     2- order of the columns of trained data
    
    """
    neighbourhood: str
    room_type: str
    minimum_nights: float
    mois: int
    voyageurs: float
    chambres: float
    lits: float
    salle_de_bains: float

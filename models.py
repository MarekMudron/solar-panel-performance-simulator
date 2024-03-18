from pydantic import BaseModel

class LocationModel(BaseModel):
    lat: float
    lon: float
    alt: float

class SolarArray(BaseModel):
    tilt: float
    azimuth: float
    nameplate:float
    gamma_pdc: float
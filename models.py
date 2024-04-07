from pydantic import BaseModel

class LocationModel(BaseModel):
    lat: float
    lon: float
    alt: float

class PanelBlock(BaseModel):
    tilt: float
    azimuth: float
    num_panels:int
    nameplate_of_one:float
    gamma_pdc_of_one: float

class String(BaseModel):
    blocks: list[PanelBlock]
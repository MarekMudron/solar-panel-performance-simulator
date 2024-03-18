from typing import Union

from fastapi import FastAPI
import simulation
from fastapi.middleware.cors import CORSMiddleware
from models import LocationModel, SolarArray

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",  # Your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)



@app.post("/simulate")
async def simulate(location: LocationModel, arrays: list[SolarArray]):
    print(location, arrays)
    output = simulation.run(location, arrays[0])
    return output

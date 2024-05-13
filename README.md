# Web App for Solar Panel Positioning - backend

This repository contains the backend code for a solar performance estimation application. The backend is implemented in Python and utilizes FastAPI, a modern, fast web framework for building APIs. The application leverages pvlib, a specialized library for solar energy system modeling, specifically employing the PVWatts model to estimate the performance of photovoltaic systems.

The server offers only single POST endpoint `/simulate`.


## Installation and Running
1. Clone the repo
2. Set Up a Virtual Environment (recommended):

    ```
    python -m venv solarenv
    source solarenv/bin/activate
    ```
3. Install the requirements

    `pip install -r requirements.txt`

    This will launch the application on a local server.

5. Run the server

    `uvicorn endpoints:app`
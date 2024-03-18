import pvlib
import pandas as pd




def run(location, model):
    
    def get_weather_data(location):
        out = pvlib.iotools.get_pvgis_tmy(location.lat, location.lon, map_variables=True)
        weather = out[0]
        weather.index = weather.index.map(lambda x: x.replace(year=2016))
        return weather
    
    weather = get_weather_data(location)
    location = pvlib.location.Location(latitude=location.lat,
                                   longitude=location.lon,
                                   altitude=location.alt)
    times = weather.index - pd.Timedelta('30min')
    solar_position = location.get_solarposition(times)
    solar_position.index += pd.Timedelta('30min')
    parameters = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_polymer']
    
    irradiance = pvlib.irradiance.get_total_irradiance(surface_tilt=model.tilt,
                                                       surface_azimuth=model.azimuth,
                                                       dni=weather['dni'],
                                                       ghi=weather['ghi'],
                                                       dhi=weather['dhi'],
                                                       solar_zenith=solar_position['apparent_zenith'],
                                                       solar_azimuth=solar_position['azimuth'])
    cell_temperature = pvlib.temperature.sapm_cell(irradiance["poa_global"],
                                                    weather['temp_air'],
                                                    weather['wind_speed'],
                                                    **parameters)
    array_power = pvlib.pvsystem.pvwatts_dc(irradiance["poa_global"], cell_temperature, model.nameplate, model.gamma_pdc)
    def get_month(data, month):
        return data[data.index.month==month]
    
    monthly_sum = array_power.resample('M').sum()
    monthly_avg_by_time_df = array_power.groupby([array_power.index.month, array_power.index.time]).mean()
    monthly_avg_by_time = {}

    for (month, time), value in monthly_avg_by_time_df.items():
        if month not in monthly_avg_by_time:
            monthly_avg_by_time[month] = []
        
        monthly_avg_by_time[month].append(value)

    return {"monthly_sum":monthly_sum, "monthly_avg_by_time":monthly_avg_by_time}
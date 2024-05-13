import pvlib
import pandas as pd

def get_weather_data(location):
    out = pvlib.iotools.get_pvgis_tmy(location.latitude, location.longitude, map_variables=True)
    weather = out[0]
    weather.index = weather.index.map(lambda x: x.replace(year=2016))
    return weather


def get_solar_position_at(location, weather_timesteps):
    times = weather_timesteps - pd.Timedelta('30min')
    solar_position = location.get_solarposition(times)
    solar_position.index += pd.Timedelta('30min')
    return solar_position;



def get_string_power(string, weather, solar_position):
    parameters = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_polymer']
    string_powers_df = None
    for block in string.blocks:
        irradiance = pvlib.irradiance.get_total_irradiance(surface_tilt=block.tilt,
                                                       surface_azimuth=block.azimuth,
                                                       dni=weather['dni'],
                                                       ghi=weather['ghi'],
                                                       dhi=weather['dhi'],
                                                       solar_zenith=solar_position['apparent_zenith'],
                                                       solar_azimuth=solar_position['azimuth'])
        cell_temperature = pvlib.temperature.sapm_cell(irradiance["poa_global"],
                                                    weather['temp_air'],
                                                    weather['wind_speed'],
                                                    **parameters)
        block_nameplate = block.nameplate_of_one * block.num_panels
        block_gamma_pdc = (block.gamma_pdc_of_one/100) 
        block_power = pvlib.pvsystem.pvwatts_dc(irradiance["poa_global"], cell_temperature, block_nameplate, block_gamma_pdc)
        if(string_powers_df is None):
            string_powers_df = block_power
        else:
            string_powers_df = string_powers_df.add(block_power)
    return string_powers_df




def get_system_power(location, strings):
    location = pvlib.location.Location(latitude=location.lat,
                                longitude=location.lon,
                                altitude=location.alt)
    
    weather = get_weather_data(location)

    solar_position = get_solar_position_at(location, weather.index)
    
    system_power_df = None;
    for string in strings:
        string_power = get_string_power(string, weather, solar_position)
        if(system_power_df is None):
            system_power_df = string_power
        else:
            system_power_df = system_power_df.add(string_power)
    return system_power_df


def run(location, strings):
    system_power_df = get_system_power(location, strings)

    monthly_sum = system_power_df.resample('M').sum()
    monthly_avg_by_time = system_power_df.groupby([system_power_df.index.month, system_power_df.index.time]).mean()

    monthly_avgs = {}
    for (month, time), value in monthly_avg_by_time.items():
        if month not in monthly_avgs:
            monthly_avgs[month] = []
        monthly_avgs[month].append(value)
    result_dict = {}
    result_dict["monthly_avgs"] = monthly_avgs
    result_dict["sums_acrross_months"] = monthly_sum.values.tolist()
    return result_dict
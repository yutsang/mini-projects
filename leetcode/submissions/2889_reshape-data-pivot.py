import pandas as pd

def pivotTable(weather: pd.DataFrame) -> pd.DataFrame:
    pivoted_weather = weather.pivot(index='month', columns='city', values='temperature')
    
    return pivoted_weather
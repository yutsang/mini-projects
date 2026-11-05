import pandas as pd

def getDataframeSize(players: pd.DataFrame) -> List[int]:
    lnum_rows, num_columns = players.shape
    return [lnum_rows, num_columns]
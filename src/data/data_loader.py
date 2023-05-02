import pandas as pd
from typing import Literal


class DataLoader:
    """
    Loads data from specified path
    """

    def load_data(self, path_to_data: str) -> pd.DataFrame:
        """
        Loads and data and unarchives it if needed
        """
        
        COMPRESSION = Literal['gzip', None]
        compression = "gzip" if path_to_data.endswith("gz") else None
        COMPRESSION = compression

        df = pd.read_csv(path_to_data, compression=COMPRESSION)

        return df

    # Неплохо бы встроить в процесс загрузки файла еще и его трансформацию и очистку

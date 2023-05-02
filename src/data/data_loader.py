import pandas as pd


class DataLoader:
    """
    Loads data from specified path
    """


    def load_data(self, path_to_data: str) -> pd.DataFrame:
        """
        Loads and data and unarchives it if needed
        """

        compression = "gzip" if path_to_data.endswith("gz") else None

        df = pd.read_csv(path_to_data, compression=compression)

        return df

    # Неплохо бы встроить в процесс загрузки файла еще и его трансформацию и очистку

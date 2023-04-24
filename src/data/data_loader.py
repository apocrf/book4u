import pandas as pd


class DataLoader:
    """
    Loads data from specified path
    """

    def load_data(path: str) -> pd.DataFrame:
        """
        Loads and data and unarchives it if needed
        """

        compression = "gzip" if path.endswith("gz") else None

        df = pd.read_csv(path, compression=compression)

        return df

    # Неплохо бы встроить в процесс загрузки файла еще и его трансформацию и очистку

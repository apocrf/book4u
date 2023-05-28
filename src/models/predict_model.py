import click

import pandas as pd

import joblib  # type: ignore


def vectorize_index(input_path: str, index: int) -> pd.DataFrame:
    """
    Turns input into vector
    :param input_path: path to data in parquet format, containing vectorized descriptions
    :param index: index of vectorized description
    """
    vectorized_book = pd.read_parquet(
        input_path,
        engine="fastparquet",
        filters=[("index", "==", index)],
        row_filter=True,
    )
    return vectorized_book


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("input_path_model", type=click.Path())
@click.argument(
    "index",
    type=click.INT,
)
def recommend_books(input_path_data: str, input_path_model: str, index: int) -> list:
    """
    :param input_path_data: path to data in parquet format,
     containing vectorized descriptions
    :param input_path_model: path to model
    :param index: index of vectorized description
    """
    vectorized_book = vectorize_index(input_path_data, index=index)
    nn_model = joblib.load(input_path_model)
    nn_prediction = nn_model.kneighbors(vectorized_book, n_neighbors=6)
    nn_prediction = list(nn_prediction[1][0][1:])
    return nn_prediction

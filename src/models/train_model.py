import click

import pandas as pd

from sklearn.neighbors import NearestNeighbors  # type: ignore

import joblib  # type: ignore


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def train_model(input_path: str, output_path: str):
    """
    Train NN model, save it in .sav format
    :param input_path:
    :param output_path:
    """
    df_vectors = pd.read_parquet(input_path)
    nn_model = NearestNeighbors()
    nn_model = nn_model.fit(df_vectors)
    joblib.dump(nn_model, output_path)

import click
import mlflow  # type: ignore
import joblib  # type: ignore
import pandas as pd

from dotenv import load_dotenv  # type: ignore
from sklearn.neighbors import NearestNeighbors  # type: ignore

load_dotenv()


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def train_model(input_path: str, output_path: str):
    """
    Train NN model, save it in .sav format
    :param input_path:
    :param output_path:
    """
    mlflow.set_tracking_uri("http://localhost:5000")

    with mlflow.start_run():
        print("start mlflow session...")

        df_vectors = pd.read_parquet(input_path)
        nn_model = NearestNeighbors()
        nn_model = nn_model.fit(df_vectors)
        joblib.dump(nn_model, output_path)
        mlflow.sklearn.log_model(
            sk_model=nn_model,
            artifact_path="model",
            registered_model_name="book_nn",
        )


if __name__ == "__main__":
    train_model()  # pylint: disable=no-value-for-parameter

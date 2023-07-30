import click
import pandas as pd

import mlflow  # type: ignore


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def make_id_mapping(input_path: str, output_path: str):
    """
    Makes id mapping file. Required for Redis.
    :param input_path: Path to read raw csv from
    :param output_path: Path to save cleansed dataframe in csv format
    """
    df_to_map = pd.read_parquet(input_path)
    df_to_map[['author', 'title', 'desc']].to_parquet(output_path)

    print("Mapping is Done!")


if __name__ == "__main__":
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("mapping_dataset")
    with mlflow.start_run() as run:
        make_id_mapping()  # pylint: disable=no-value-for-parameter

import click
import pandas as pd

import mlflow  # type: ignore


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path_1", type=click.Path())
@click.argument("output_path_2", type=click.Path())
@click.argument("output_path_3", type=click.Path())
def make_full_id_mapping(
    input_path: str, output_path_1: str, output_path_2: str, output_path_3: str
):
    """
    Makes id mapping file. Required for Redis.
    :param input_path: Path to read dataframe from
    :param output_path_1: Path to save dataframe
    :param output_path_2: Path to save dataframe
    :param output_path_3: Path to save dataframe
    """
    df_to_map = pd.read_parquet(input_path)
    # "../data/interim/GoodReads_books_clean.parquet"
    df_to_map[["author", "title", "desc"]].to_parquet(output_path_1)
    # "../data/interim/full_id_mapping.parquet"
    id_title_mapping_data = df_to_map[["title"]]
    id_title_mapping_data.to_parquet(output_path_2)
    # "../data/interim/id_title_mapping_data.parquet"
    title_id_mapping_data = id_title_mapping_data.reset_index()
    title_id_mapping_data = title_id_mapping_data.set_index("title")
    title_id_mapping_data.to_parquet(output_path_3)
    # "../data/interim/title_id_mapping_data.parquet"
    print("Mapping is Done!")


if __name__ == "__main__":
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("full_id_mapping")
    with mlflow.start_run() as run:
        make_full_id_mapping()  # pylint: disable=no-value-for-parameter

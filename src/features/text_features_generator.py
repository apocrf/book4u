import click
import pandas as pd


def verbalize_rating(rating: int) -> str:
    """
    Turn numerical rating into verbal representation.
    :param rating: rating in numerical format
    :return: rating in verbal representation
    """
    rating_verbalized = " Readers rated the book as "
    if rating >= 4.5:
        rating_verbalized += "outstanding."
    elif 3.5 <= rating < 4.5:
        rating_verbalized += "good."
    elif 2.5 <= rating < 3.5:
        rating_verbalized += "average."
    elif 1.5 <= rating < 2.5:
        rating_verbalized += "bad."
    elif 0 < rating < 1.5:
        rating_verbalized += "awful."
    else:
        rating_verbalized = " This book has not been rated."
    return rating_verbalized


def generate_extended_description(df_original: pd.DataFrame) -> pd.Series:
    """
    Combine book genre, description and rating into single string.
    :param df_original: original pd.DataFrame to process
    :return: pd.Series with a column with extended book description
    """
    extended_description = (
        "This book belongs to the following genres: "
        + df_original["genre"].str.replace(",", ", ")
        + ". Description of the book: "
        + df_original["desc"]
        + df_original["rating"].apply(verbalize_rating)
    )
    return extended_description


def generate_maximally_extended_description(df_original: pd.DataFrame) -> pd.Series:
    """
    Combine book title, genre, description, rating and author's name into single string.
    :param df_original: original pd.DataFrame to process
    :return: pd.Series with a column with extended book description
    """
    maximally_extended_description = (
        "The book is titled "
        + df_original["title"]
        + " by "
        + df_original["author"]
        + ". "
        + generate_extended_description(df_original)
    )
    return maximally_extended_description


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def create_extended_df(input_path: str, output_path: str):
    """
    Create and save pd.Dataframe containing extended book descriptions
    in .parquet format.
    :param input_path: Path to read raw .parquet from
    :param output_path: Path to save cleansed
    dataframe in .parquet format
    """
    df_to_generate_from = pd.read_parquet(input_path)

    extended_description = generate_extended_description(df_to_generate_from)
    extended_description_max = generate_maximally_extended_description(
        df_to_generate_from
    )
    df_extended_description = pd.DataFrame(data=extended_description, columns=["desc"])
    df_extended_description_max = pd.DataFrame(
        data=extended_description_max, columns=["desc"]
    )

    df_extended_description.to_parquet(output_path)
    df_extended_description_max.to_parquet(output_path.replace("_", "_max_"))

    print("Text extension is done! Results are saved!")


if __name__ == "__main__":
    create_extended_df()  # pylint: disable=no-value-for-parameter

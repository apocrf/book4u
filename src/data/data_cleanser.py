"""
Data Cleanser module

Contains functions to clean raw data.

Contains following functions:
    - drop_important_nans
    - drop_repeated_books
    - drop_useless_columns
    - drop_non_english_books
    - cleanse_data
"""
import re
import click
import pandas as pd


def drop_important_nans(df_to_process: pd.DataFrame) -> pd.DataFrame:
    """
    Drop all rows containing Nans in book description, genre, author or title
    :param df_to_process: pd.DataFrame to drop Nans from
    :return: pd.DataFrame with no Nans
    """
    total_nans_dropped = (
        df_to_process["desc"].isna()
        | df_to_process["genre"].isna()
        | df_to_process["author"].isna()
        | df_to_process["title"].isna()
    ).sum()
    print(f"Amount of rows with Nans dropped = {total_nans_dropped}")

    df_to_process = df_to_process.dropna(subset=["desc", "genre", "author", "title"])

    return df_to_process


def drop_repeated_books(df_to_process: pd.DataFrame) -> pd.DataFrame:
    """
    Drop all duplicates based on author/title combination
    :param df_to_process: pd.DataFrame to drop repeated values from
    :return: pd.DataFrame with no repeated values
    """
    total_dupes_dropped = df_to_process.duplicated(subset=["author", "title"]).sum()
    print(f"Amount of duplicated rows dropped = {total_dupes_dropped}")

    df_to_process = df_to_process.drop_duplicates(subset=["author", "title"])

    return df_to_process


def drop_useless_columns(
    df_to_process: pd.DataFrame, columns: tuple = ("bookformat", "reviews", "pages")
) -> pd.DataFrame:
    """
    Drop all columns considered useless.
    By default it's bookformat, reviews and pages columns
    :param df_to_process: pd.DataFrame to drop columns from
    :param columns: columns considered useless
    :return: pd.DataFrame with no useless columns
    """
    print("Names of dropped columns: ", end="")
    print(*columns, sep=", ")

    df_to_process = df_to_process.drop(list(columns), axis=1)

    return df_to_process


def drop_non_english_books(df_to_process: pd.DataFrame) -> pd.DataFrame:
    """
    Drop rows containing unintelligible letters in title, desc and author columns
    :param df_to_process: pd.DataFrame to drop values from
    :return: pd.DataFrame with no non-english values
    """
    pattern = r"[^a-zA-Z0-9 \]\[+$#*/?!&\-:;,\.\'\")(]"
    total_unintelligible_rows = (
        df_to_process["title"].apply(lambda x: bool(re.search(pattern, x)))
        | df_to_process["author"].apply(lambda x: bool(re.search(pattern, x)))
        | df_to_process["desc"].apply(lambda x: bool(re.search(pattern, x)))
    ).sum()
    print(
        f"""Amount of rows containing non-english letters dropped = 
        {total_unintelligible_rows}"""
    )

    for _ in ("title", "desc", "author"):
        df_to_process = df_to_process[
            df_to_process[_].apply(lambda x: not bool(re.search(pattern, x)))
        ]

    return df_to_process


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def cleanse_data(input_path: str, output_path: str):
    """
    Successively executes drop_important_nans, drop_repeated_books,
    drop_useless_columns, drop_non_english_books functions.
    Realizes preprocessing of raw data.
    :param input_path: Path to read raw csv from
    :param output_path: Path to save cleansed dataframe in csv format
    """
    df_to_cleanse = pd.read_csv(input_path)

    df_to_cleanse = drop_important_nans(df_to_cleanse)
    df_to_cleanse = drop_repeated_books(df_to_cleanse)
    df_to_cleanse = drop_useless_columns(df_to_cleanse)
    df_to_cleanse = drop_non_english_books(df_to_cleanse)
    df_to_cleanse = df_to_cleanse.reset_index(drop=True)

    if output_path.endswith("csv"):
        df_to_cleanse.to_csv(output_path)
    elif output_path.endswith("parquet"):
        df_to_cleanse.to_parquet(output_path)
    else:
        print("Only .csv and .parquet are allowed as save formats.")
        return
    print("Cleaning is Done!")


if __name__ == "__main__":
    cleanse_data()  # pylint: disable=no-value-for-parameter

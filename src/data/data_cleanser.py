import re
import pandas as pd


class DataCleanser:
    """
    Testing data for impurities &
    Cleaning data from impurities
    """

    def __init__(self, original_df: pd.DataFrame):
        self.df = original_df

    def drop_important_nans(self):
        """
        Inplace drop all rows containing Nans in book description, genre, author or title
        """

        total_nans_dropped = (
            self.df["desc"].isna()
            | self.df["genre"].isna()
            | self.df["author"].isna()
            | self.df["title"].isna()
        ).sum()
        print(f"Amount of rows with Nans dropped = {total_nans_dropped}")

        self.df = self.df.dropna(subset=["desc", "genre", "author", "title"])

    def drop_repeated_books(self):
        """
        Inplace drop all duplicates based on author/title combination
        """

        total_dupes_dropped = self.df.duplicated(subset=["author", "title"]).sum()
        print(f"Amount of duplicated rows dropped = {total_dupes_dropped}")

        self.df = self.df.drop_duplicates(subset=["author", "title"])

    def drop_useless_columns(self, columns: tuple = ("bookformat", "reviews", "pages")):
        """
        Inplace drop bookformat, reviews and pages columns
        """

        print("Names of dropped columns: ", end="")
        print(*columns, sep=", ")

        self.df = self.df.drop(columns, axis=1)

    def drop_non_english_books(self):
        """
        Inplace drop rows containing unintelligible letters
        """

        pattern = r"[^a-zA-Z0-9 \]\[+$#*/?!&\-:;,\.\'\")(]"
        total_unintelligible_rows = (
            self.df["title"].apply(lambda x: bool(re.search(pattern, x)))
            | self.df["author"].apply(lambda x: bool(re.search(pattern, x)))
            | self.df["desc"].apply(lambda x: bool(re.search(pattern, x)))
        ).sum()
        print(
            f"""Amount of rows containing non-english letters dropped = 
            {total_unintelligible_rows}"""
        )

        self.df = self.df[
            self.df["title"].apply(lambda x: not bool(re.search(pattern, x)))
        ]
        self.df = self.df[
            self.df["desc"].apply(lambda x: not bool(re.search(pattern, x)))
        ]
        self.df = self.df[
            self.df["author"].apply(lambda x: not bool(re.search(pattern, x)))
        ]

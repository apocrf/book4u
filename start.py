import src

RAW_DATA_PATH = "data/raw/GoodReads_100k_books.csv"
CLEANED_DATA_PATH = "data/interim/GoodReads_books_clean.csv"

if __name__ == "__main__":
    src.cleanse_data(RAW_DATA_PATH, CLEANED_DATA_PATH)

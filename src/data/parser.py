from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
import pandas as pd
import requests
from tqdm import tqdm

df_main = pd.DataFrame(
    columns=[
        "isbn",
        "title",
        "authors",
        "publisher",
        "genres",
        "rating",
        "people_rated",
        "annotation",
    ]
)
df_temp = pd.DataFrame(
    columns=[
        "isbn",
        "title",
        "authors",
        "publisher",
        "genres",
        "rating",
        "people_rated",
        "annotation",
    ]
)

try:
    df_main = pd.read_parquet("../../data/raw/books.parquet")
except FileNotFoundError:
    df_main.to_parquet("../../data/raw/books.parquet")


def go(book_id):
    global df_temp
    data = requests.get("https://www.labirint.ru/books/" + str(book_id), timeout=10)
    soup = BeautifulSoup(data.text, features="html.parser")
    row = {}

    try:
        genres = soup.find(name="div", attrs={"id": "thermometer-books"}).find_all(
            name="span", attrs={"itemprop": "title"}
        )
        if not genres:
            return
    except (KeyError, AttributeError):
        return
    genres = [_.text for _ in genres]
    if genres[0] != "Книги":
        return
    if genres[1] == "Художественная литература":
        genres = genres[1:]
        row["genres"] = "/".join(genres)
    if len(genres) < 3:
        return
    if genres[2] == "Детская художественная литература":
        genres = genres[2:]
        row["genres"] = "/".join(genres)
    else:
        return

    try:
        title = soup.find(name="div", attrs={"id": "product-about"}).h2.text[19:-1]
    except (AttributeError, KeyError, SyntaxError):
        return
    row["title"] = title

    annotation = (
        soup.find(name="div", attrs={"id": "product-about"}).find_all("p")[-1].text
    )
    if len(annotation) <= 100:
        return
    row["annotation"] = annotation

    authors = [
        _.text for _ in soup.find_all(name="a", attrs={"data-event-label": "author"})
    ]
    if authors:
        row["authors"] = "/".join(authors)

    publisher = soup.find(name="a", attrs={"data-event-label": "publisher"})
    if publisher:
        row["publisher"] = publisher

    rating = float(soup.find(name="div", attrs={"id": "rate"}).text)
    row["rating"] = rating

    rated = soup.find(name="div", attrs={"id": "product-rating-marks-label"}).text
    rated = int(rated.split()[-1][:-1])
    row["people_rated"] = rated

    isbn = soup.find(name="div", attrs={"class": "isbn"}).text.split()[1]
    row["isbn"] = isbn

    df_temp = pd.concat([df_temp, pd.DataFrame(data=row, index=[book_id])])


# Первый трейсбэк на странице 622 - не было жанрового описания
# , поправил такое исключение
# Второй - длина списка жанров была короче 3-х. Поправил.
# Остановка на странице : 172_500

pool = ThreadPool()
counter = 0
start = 172_500
finish = 172_521
for i in tqdm(range(8_625, 46_601, 1)):
    pool.map(go, range(start, finish))
    start += 20
    finish += 20
    counter += 1
    if counter == 5:
        counter = 0
        if len(df_temp) == 0:
            continue
        df_main = pd.read_parquet("../../data/raw/books.parquet")
        df_main = pd.concat([df_main, df_temp])
        df_main.to_parquet("../../data/raw/books.parquet")
        del df_main
        df_temp = pd.DataFrame(
            columns=[
                "isbn",
                "title",
                "authors",
                "publisher",
                "genres",
                "rating",
                "people_rated",
                "annotation",
            ]
        )

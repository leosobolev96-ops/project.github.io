import requests
from bs4 import BeautifulSoup
import pandas as pd

HOME_URL = "http://books.toscrape.com/index.html"

RATINGS = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def get_books_data():
    books_list = []

    
    response = requests.get(HOME_URL)
    soup = BeautifulSoup(response.content, "html.parser")

    
    books = soup.find_all("article", class_="product_pod")[:5]

    for book in books:

        
        title = book.find("h3").find("a")["title"]

        
        price_text = book.find("p", class_="price_color").text
        price = float(price_text.replace("£", ""))

        
        img_src = book.find("img")["src"]
        img_url = "http://books.toscrape.com/" + img_src.replace("../", "")

        
        rating_class = book.find("p", class_="star-rating")["class"][1]
        rating = RATINGS.get(rating_class, 0)

        
        link = book.find("h3").find("a")["href"]
        book_url = "http://books.toscrape.com/catalogue/" + link.replace("catalogue/", "")

        book_response = requests.get(book_url)
        book_soup = BeautifulSoup(book_response.content, "html.parser")

        desc_block = book_soup.find("div", id="product_description")

        if desc_block:
            description = desc_block.find_next("p").text
        else:
            description = "Нет описания"

        books_list.append({
            "Название": title,
            "Цена": price,
            "Рейтинг": rating,
            "Фото": img_url,
            "Описание": description[:150] + "..."
        })

    return books_list


data = get_books_data()

df = pd.DataFrame(data)
df.to_excel("books.xlsx", index=False)

print("Excel файл успешно создан")
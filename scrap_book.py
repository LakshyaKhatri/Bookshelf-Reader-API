from bs4 import BeautifulSoup
import urllib
import requests


def getTitleImageAndISBN(book_title):
    search_txt = book_title + " book amazon india"
    search_txt = urllib.parse.quote_plus(search_txt)
    url = 'https://google.com/search?q=' + search_txt

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    book_amazon_link = ""
    for link in soup.find_all('a'):
        if "amazon.in" in link.get('href'):
            book_amazon_link = link.get('href')
            break

    isbn = book_amazon_link[book_amazon_link.find("dp/") + 3: book_amazon_link.find('&')]
    book_data_url = "https://www.abebooks.com/servlet/SearchResults?sts=t&isbn=" + isbn

    response = requests.get(book_data_url)
    soup = BeautifulSoup(response.text, "html.parser")

    response = requests.get(book_data_url)
    soup = BeautifulSoup(response.text, "html.parser")

    imageUrl = ''
    for imgTag in soup.find_all("img"):
        if imgTag.get('class') == ['srp-item-image', ]:
            imageUrl = imgTag.get('src')
            break

    title = soup.h2.span.text
    title = title.title()

    return (title, imageUrl, isbn)

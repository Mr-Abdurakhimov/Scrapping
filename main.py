import json
import time
from datetime import datetime
from bs4 import BeautifulSoup
import requests

start_time = time.time()


def GetInfo(headers):
    info_list = []
    date = datetime.now().strftime("%d_%m_%y")
    count = 0
    for i in range(1, 6):
        response = requests.get(f"https://www.labirint.ru/books/?id_genre=2994&nrd=1&page={i}", headers=headers)
        soup = BeautifulSoup(response.content, "lxml")
        page = soup.find_all("div", class_="products-row-outer responsive-cards")[2]
        cards = page.find_all("div", class_="card-column card-column_gutter col-xs-6 col-sm-3 col-md-1-5 col-xl-2")
        for card in cards:
            count += 1
            title = card.find("div", class_="product-cover").find("span", class_="product-title").text.strip()
            try:
                author = card.find("div", class_="product-author").find("span").text.strip()
            except:
                author = "Автор не указан"
            try:
                publishing_company = card.find("div", class_="product-pubhouse").find("span").text.strip()
            except:
                publishing_company = "Компания не указана"
            price = card.find("span", class_="price-val").text.strip()
            info_list.append({
                "title": title,
                "author": author,
                "publishing_company": publishing_company,
                "price": price
            })
            print(f"{count}: {title} information is ready")
    with open(f"{date}__artbooks.json", "w", encoding="utf-8") as file:
        json.dump(info_list, file, ensure_ascii=False, indent=4)


def main():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49"
    }
    GetInfo(headers)
    print(f"Затраченное время на выполнение скрипта: {time.time()-start_time}")

if __name__ == "__main__":
    main()

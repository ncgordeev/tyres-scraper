from main_class import TyreScraper

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from config import DATA_PATH, SHINSERVICE
import time


class ShinserviceScraper(TyreScraper):

    def scrape_page(self, page_url: str) -> None:
        number_of_page = "?page="
        page_count = 0
        url = f"{page_url}{number_of_page}{page_count}"
        user_agent = UserAgent()
        add_user_agent = user_agent.random
        headers = {
            "User-Agent": add_user_agent,
        }
        page_response = requests.get(url, headers=headers)
        main_url = "https://www.shinservice.ru"
        tyres_dict = {}
        if page_response.status_code == 200:
            soup = BeautifulSoup(page_response.text, "html.parser")
            pagination = soup.find_all(class_="stp-pagination-item")
            for index in range(len(pagination) + 1):
                page_count += 1
                url = f"{page_url}{number_of_page}{page_count}"
                page_response = requests.get(url, headers=headers)
                soup = BeautifulSoup(page_response.text, "html.parser")

                tyres = soup.find_all(class_="stp-catalog-card-goods")
                for tyre in tyres:
                    title = tyre.find(class_="stp-catalog-card-title").text.strip()
                    tyre_size = tyre.find("span", class_="goods-attribute-value").text.strip()
                    price = tyre.find(class_="stp-price_1").text.strip().replace(" ", "")
                    raw_link = tyre.find(class_="title__Link-sc-12e08d15-1 cQLJhK")
                    tyre_link = f"{main_url}{raw_link.get('href')}"
                    tyres_dict[title] = tyre_size, price, tyre_link
                    time.sleep(0.2)
                self.save_data(tyres_dict, DATA_PATH)
        else:
            print("Failed to retrieve the webpage. Status code:", page_response.status_code)
            exit()

    def choose_tyre_size(self, page_url: str):
        tyre_width = self.get_numeric_input("Введите ширину: ")
        tyre_high = self.get_numeric_input("Введите высоту профиля: ")
        tyre_diameter = self.get_numeric_input("Введите диаметр: ")
        tyre_season = input("Введите сезон: зима/лето: ").strip().lower()

        if tyre_season == "зима":
            return (f"{page_url}/diameter-is-{tyre_diameter}/profile-is-{tyre_high}"
                    f"/season-is-winter/width-is-{tyre_width}/")
        elif tyre_season == "лето":
            return (f"{page_url}/diameter-is-{tyre_diameter}/profile-is-{tyre_high}"
                    f"/season-is-summer/width-is-{tyre_width}/")
        else:
            print("Вы не выбрали сезонность. Загружены данные по всем сезонам.")
            return f"{page_url}/diameter-is-{tyre_diameter}/profile-is-{tyre_high}/width-is-{tyre_width}/"


c = ShinserviceScraper()
scraping_url = c.choose_tyre_size(SHINSERVICE)
print(scraping_url)
c.scrape_page(scraping_url)
print(c.get_data(DATA_PATH))

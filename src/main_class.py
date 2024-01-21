import json
from json import JSONDecodeError

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from config import DATA_PATH, SHINSERVICE


class TyreScraper:

    def save_data(self, data: dict, file_path: str) -> None:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                read_data = json.load(file)
        except JSONDecodeError:
            read_data = {}

        read_data.update(data)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(read_data, file, indent=2, ensure_ascii=False)

    def get_data(self, file_path: str):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                raw_data = json.load(file)
                print(len(raw_data))  # may delete
                for title, price in raw_data.items():
                    print(f"{title} - {price}")
        except JSONDecodeError:
            print("Данные отсутствуют!")


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
                    price = tyre.find(class_="stp-price_1").text.strip().replace(" ", "")
                    raw_link = tyre.find(class_="title__Link-sc-12e08d15-1 cQLJhK")
                    tyre_link = f"{main_url}{raw_link.get('href')}"
                    tyres_dict[title] = price, tyre_link
                self.save_data(tyres_dict, DATA_PATH)
        else:
            print("Failed to retrieve the webpage. Status code:", page_response.status_code)
            exit()

    @staticmethod
    def choose_tyre_size(page_url: str):
        tyre_with = input("Введите ширину: ")
        tyre_high = input("Введите высоту профиля: ")
        tyre_diameter = input("Введите диаметр: ")
        tyre_season = input("Введите сезон: зима/лето: ").strip().lower()

        if tyre_season == "зима":
            return (f"{page_url}/diameter-is-{tyre_diameter}/profile-is-{tyre_high}"
                    f"/season-is-winter/width-is-{tyre_with}/")
        elif tyre_season == "лето":
            return (f"{page_url}/diameter-is-{tyre_diameter}/profile-is-{tyre_high}"
                    f"/season-is-summer/width-is-{tyre_with}/")
        else:
            print("Вы не выбрали сезонность. Загружены данные по всем сезонам.")
            return f"{page_url}/diameter-is-{tyre_diameter}/profile-is-{tyre_high}/width-is-{tyre_with}/"

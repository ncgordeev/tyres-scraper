import json

import requests
from bs4 import BeautifulSoup
from config import DATA_PATH, SHINSERVICE


class ShinserviceScraper:

    def __init__(self, title: str) -> None:
        self.title = title

    def scrape_page(self, page_url: str) -> None:
        url = page_url
        page_response = requests.get(url)
        tires_dict = {}
        if page_response.status_code == 200:
            soup = BeautifulSoup(page_response.text, "html.parser")
            tires = soup.find_all(class_="stp-catalog-card-goods")
            for tire in tires:
                title = tire.find(class_="stp-catalog-card-title").text.strip()
                price = tire.find(class_="stp-price_1").text.strip()
                tires_dict[title] = price
            self.save_data(tires_dict, DATA_PATH)
        else:
            print("Failed to retrieve the webpage. Status code:", page_response.status_code)
            exit()

    @classmethod
    def save_data(cls, data: dict, file_path: str) -> None:
        with open(file_path, "a", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    @staticmethod
    def choose_tire_size(page_url: str):
        tire_with = int(input("Введите ширину: "))
        tire_high = int(input("Введите высоту профиля: "))
        tire_diameter = int(input("Введите диаметр: "))
        tire_season = input("Введите сезон: зима/лето: ").strip().lower()

        if tire_season == "зима":
            return (f"{page_url}/diameter-is-{tire_diameter}/profile-is-{tire_high}"
                    f"/season-is-winter/width-is-{tire_with}/")
        elif tire_season == "лето":
            return (f"{page_url}/diameter-is-{tire_diameter}/profile-is-{tire_high}"
                    f"/season-is-summer/width-is-{tire_with}/")
        else:
            print("Вы не выбрали сезонность. Загружены данные по всем сезонам.")
            return f"{page_url}/diameter-is-{tire_diameter}/profile-is-{tire_high}/width-is-{tire_with}/"


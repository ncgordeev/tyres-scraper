from abc import ABC, abstractmethod
import json
from json import JSONDecodeError


class BaseScraper(ABC):

    @abstractmethod
    def scrape_page(self, page_url: str):
        pass

    @abstractmethod
    def choose_tyre_size(self, page_url: str):
        pass


class TyreScraper(ABC):

    def scrape_page(self, page_url: str):
        pass

    def choose_tyre_size(self, page_url: str):
        pass

    def get_numeric_input(self, prompt: str) -> str:
        while True:
            try:
                value = input(prompt)
                if value.isdigit():
                    return value
            except ValueError:
                print("Пожалуйста, введите число.")

    def save_data(self, data: dict, file_path: str) -> None:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                read_data = json.load(file)
        except JSONDecodeError:
            read_data = {}

        for title, info in data.items():
            read_data[title] = info

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(read_data, file, indent=2, ensure_ascii=False)

    def get_data(self, file_path: str):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                raw_data = json.load(file)
                print(len(raw_data))  # may delete
                sorted_data_by_name = {key: raw_data[key] for key in sorted(raw_data)}
                for title, price in sorted_data_by_name.items():
                    print(f"{title} - {price}")
        except JSONDecodeError:
            print("Данные отсутствуют!")

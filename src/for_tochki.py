from main_class import TyreScraper

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from config import DATA_PATH
import time


class ForTochki(TyreScraper):

    def scrape_page(self, page_url: str) -> None:
        user_agent = UserAgent()
        headers = {
            "User-Agent": user_agent.random,
        }
        main_url = "https://www.4tochki.ru"
        tyres_dict = {}

        page_counter = 1
        while True:
            current_url = f"{page_url}&page={page_counter}&url=%2Fcatalog%2Fsearch%2F"
            print(current_url)

            page_response = requests.get(current_url, headers=headers)
            if page_response.status_code != 200:
                print(f"Failed to fetch page {current_url}. Status code: {page_response.status_code}")
                break

            soup = BeautifulSoup(page_response.text.strip().replace("\\n", "").replace("\\", ""), "html.parser")
            tyres = soup.find_all("div", class_="b-item__wrap")

            for tyre in tyres:
                title = tyre.find("a", class_="b-item__name-link").text.strip()
                tyre_size = tyre.find("div", class_="b-item__size").text.strip()
                price = tyre.find("span", class_="b-item__price-text").text.strip()
                raw_link = tyre.find(class_="b-item__mark-img")
                catalog_link = raw_link.contents[1]
                tyre_link = f"{main_url}{catalog_link.get('href')}"
                tyres_dict[title] = tyre_size, price, tyre_link
                time.sleep(0.2)

            self.save_data(tyres_dict, DATA_PATH)

            # Check for the next page button
            next_page = soup.find("button", class_="doSearch_next")
            if not next_page:
                break

            page_counter += 1

    def choose_tyre_size(self):
        tyre_width = self.get_numeric_input("Введите ширину: ")
        tyre_high = self.get_numeric_input("Введите высоту профиля: ")
        tyre_diameter = self.get_numeric_input("Введите диаметр: ")
        tyre_season = input("Введите сезон: зима/лето: ").strip().lower()

        if tyre_season == "зима":
            return (f"https://www.4tochki.ru/catalog/search/?Tsh={tyre_width}&Tprof={tyre_high}&Td={tyre_diameter}"
                    f"&season%5B2%5D=1&autosearch_car=&search_mark=0&autosearch_car=&DSh=&Dd=&Dpcd=&et=&dia="
                    f"&autosearch_car=&search_mark"
                    f"=0&search_mark=0&Stsh={tyre_width}&Stprof={tyre_high}&Std={tyre_diameter}&autosearch_car="
                    f"&search_mark=0&autosearch_car=&ComplectationId=&action_=search%2Ftyres&thread=tyres&sort="
                    f"popularity&order=desc&actionId=&searchType=param&filter_cost_from=1000&filter_cost_to=100000&cae="
                    f"&stud%5B0%5D=0")
        elif tyre_season == "лето":
            return (f"https://www.4tochki.ru/catalog/search/?Tsh={tyre_width}&Tprof={tyre_high}&Td={tyre_diameter}"
                    f"&season%5B2%5D=2&autosearch_car=&search_mark=0&autosearch_car=&DSh=&Dd=&Dpcd=&et=&dia="
                    f"&autosearch_car=&search_mark"
                    f"=0&search_mark=0&Stsh={tyre_width}&Stprof={tyre_high}&Std={tyre_diameter}&autosearch_car="
                    f"&search_mark=0&autosearch_car=&ComplectationId=&action_=search%2Ftyres&thread=tyres&sort="
                    f"popularity&order=desc&actionId=&searchType=param&filter_cost_from=1000&filter_cost_to=100000&cae="
                    f"&stud%5B0%5D=0")
        else:
            print("Вы не выбрали сезонность. Загружены данные по всем сезонам.")
            return (f"https://www.4tochki.ru/catalog/search/?Tsh={tyre_width}&Tprof={tyre_high}&Td={tyre_diameter}"
                    f"&autosearch_car=&search_mark=0&autosearch_car=&DSh=&Dd=&Dpcd=&et=&dia=&autosearch_car=&search_mark"
                    f"=0&search_mark=0&Stsh={tyre_width}&Stprof={tyre_high}&Std={tyre_diameter}&autosearch_car="
                    f"&search_mark=0&autosearch_car=&ComplectationId=&action_=search%2Ftyres&thread=tyres&sort="
                    f"popularity&order=desc&actionId=&searchType=param&filter_cost_from=1000&filter_cost_to=100000&cae="
                    f"&stud%5B0%5D=0")


f = ForTochki()
scraping_url = f.choose_tyre_size()
print(scraping_url)
f.scrape_page(scraping_url)
print(f.get_data(DATA_PATH))

# f"https://www.4tochki.ru/catalog/search/?Tsh=&Tprof=&Td=&autosearch_car=&search_mark=0&autosearch_car=&DSh=&Dd=&Dpcd=&et=&dia=&autosearch_car=&search_mark=0&search_mark=0&Stsh=&Stprof=&Std=&autosearch_car=&search_mark=0&autosearch_car=&ComplectationId=&action_=search%2Ftyres&thread=tyres&sort=popularity&order=desc&actionId=&searchType=param&filter_cost_from=1000&filter_cost_to=100000&cae=&stud%5B0%5D=0&page=1&url=%2Fcatalog%2Fsearch%2F"
# f"https://www.4tochki.ru/catalog/search/?Tsh=&Tprof=&Td=&season%5B2%5D=2&autosearch_car=&search_mark=0&autosearch_car=&DSh=&Dd=&Dpcd=&et=&dia=&autosearch_car=&search_mark=0&search_mark=0&Stsh=&Stprof=&Std=&autosearch_car=&search_mark=0&autosearch_car=&ComplectationId=&action_=search%2Ftyres&thread=tyres&sort=popularity&order=desc&actionId=&searchType=param&filter_cost_from=1000&filter_cost_to=100000&cae=&page=1&url=%2Fcatalog%2Fsearch%2F"
# f"https://www.4tochki.ru/catalog/search/?Tsh=&Tprof=&Td=&season%5B1%5D=1&autosearch_car=&search_mark=0&autosearch_car=&DSh=&Dd=&Dpcd=&et=&dia=&autosearch_car=&search_mark=0&search_mark=0&Stsh=&Stprof=&Std=&autosearch_car=&search_mark=0&autosearch_car=&ComplectationId=&action_=search%2Ftyres&thread=tyres&sort=popularity&order=desc&actionId=&searchType=param&filter_cost_from=1000&filter_cost_to=100000&cae=&stud%5B0%5D=0&page=1&url=%2Fcatalog%2Fsearch%2F"
# f"https://www.4tochki.ru/catalog/search/?Tsh=195&Tprof=65&Td=15&autosearch_car=&search_mark=0&autosearch_car=&DSh=&Dd=&Dpcd=&et=&dia=&autosearch_car=&search_mark=0&search_mark=0&Stsh=195&Stprof=65&Std=15&autosearch_car=&search_mark=0&autosearch_car=&ComplectationId=&action_=search%2Ftyres&thread=tyres&sort=popularity&order=desc&actionId=&razmer%5B%5D=62&searchType=param&filter_cost_from=1000&filter_cost_to=100000&cae=&stud%5B0%5D=0&page=3&url=%2Fcatalog%2Fsearch%2F"

import string

import requests
from bs4 import BeautifulSoup


class WikipediaAnimals:
    def __init__(self):
        self.__base_url = "https://ru.wikipedia.org"
        self.__link = f"{self.__base_url}/wiki/Категория:Животные_по_алфавиту"

    def __iter__(self):
        return self

    def __next__(self):
        response = requests.get(self.__link)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        content_div = soup.find("div", class_="mw-category mw-category-columns")
        animals_text = content_div.get_text()
        animals = [
            animal
            for animal in animals_text.split("\n")
            if len(animal) > 1 and animal[0] not in string.ascii_uppercase
        ]
        if len(animals) == 0:
            raise StopIteration
        try:
            self.__link = (
                self.__base_url + soup.find("a", string="Следующая страница")["href"]
            )
        except KeyError:
            raise StopIteration
        return animals


def count_animals() -> dict[str, int]:
    animals_count = {}
    for animals in WikipediaAnimals():
        print(animals)
        print(animals_count)
        for animal in animals:
            first_letter = animal[0]
            animals_count[first_letter] = animals_count.get(first_letter, 0) + 1
    return animals_count


def write_data_to_csv(filepath: str, data: dict):
    with open(filepath, "w") as file:
        for i in data:
            file.write(f"{i},{data[i]}\n")


if __name__ == "__main__":
    write_data_to_csv("task2/beasts.csv", count_animals())

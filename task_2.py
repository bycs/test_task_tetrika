from bs4 import BeautifulSoup

import requests


def get_html(url: str) -> str | bool:
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print("Error")
        return False


def get_soup(html: str):
    soup = BeautifulSoup(html, "html.parser")
    animals_group = soup.find("div", class_="mw-category mw-category-columns")
    try:
        next_page_url = soup.find("a", text="Следующая страница").get("href")
    except AttributeError:
        next_page_url = False
    return animals_group, next_page_url


def get_number_animals():
    base_url = "https://ru.wikipedia.org"
    animals_url = base_url + "/w/index.php?title=Категория:Животные_по_алфавиту"
    alphabet = [chr(i) for i in range(ord("А"), ord("А") + 32)]

    html = get_html(animals_url)
    animals_group, next_page_url = get_soup(html)

    number_animals = {'Ё': 0}
    for literal in alphabet:
        number_animals[literal] = 0

    while next_page_url:
        html = get_html(base_url + next_page_url)
        animals_group, next_page_url = get_soup(html)

        for animal in animals_group.find_all("li"):
            try:
                number_animals[animal.text[0]] += 1
            except KeyError:
                print(f"'{animal.text}' не начитается с буквы в русского алфавита")
    return number_animals


if __name__ == "__main__":
    number_of_animals = get_number_animals()
    for key, value in number_of_animals.items():
        if value:
            print(f"{key}: {value}")

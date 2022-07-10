from bs4 import BeautifulSoup

import requests


def get_html(url: str) -> str | bool:
    """
    get_html() принимает URL-адрес в виде строки и возвращает HTML-код страницы в виде строки или
    False, если произошла ошибка.

    :param url: str - URL страницы, которую нужно получить
    :type url: str
    :return: html-код страницы.
    """
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print("Error")
        return False


def get_soup(html: str) -> tuple[BeautifulSoup, str | bool]:
    """
    get_soup берет строку HTML-кода, анализирует ее с помощью BeautifulSoup
    и возвращает объект BeautifulSoup. Он также находит ссылку
    на следующую страницу и возвращает ее в виде строки.
    Если ссылки на следующую страницу нет, возвращает False.

    :param html: str - html код страницы
    :type html: str
    :return: Кортеж из двух элементов:
        1. Объект BeautifulSoup
        2. URL следующей страницы или False, если следующей страницы нет
    """
    soup = BeautifulSoup(html, "html.parser")
    animals_group = soup.find("div", class_="mw-category mw-category-columns")
    try:
        next_page_url = soup.find("a", text="Следующая страница").get("href")
    except AttributeError:
        next_page_url = False
    return animals_group, next_page_url


def get_number_animals() -> dict[str, int]:
    """
    Получается количество животных в русской Википедии,
    сгруппированы по первой букве имени
    :return: Словарь с количеством животных на каждую букву русского алфавита.
    """
    base_url = "https://ru.wikipedia.org"
    animals_url = base_url + "/w/index.php?title=Категория:Животные_по_алфавиту"
    alphabet = [chr(i) for i in range(ord("А"), ord("А") + 32)]

    html = get_html(animals_url)
    animals_group, next_page_url = get_soup(html)

    number_animals = {"Ё": 0}
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

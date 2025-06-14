import os
from pathlib import Path

from bs4 import BeautifulSoup


def get_user_input() -> tuple[list[str], str]:
    list_names = input(
        "(Имена списков будут присваиваться html файлам в алфавитном порядке html файлов!)\nВведите имя списка или имена списка (через пробелы): "
    )
    print("\n")
    output_type = input("Введите тип вывода (mdt, md): ")
    return list_names.split(), output_type


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def get_html_paths() -> list[str]:
    paths = list()
    for file in os.listdir("./html"):
        if file.endswith(".html"):
            paths.append(f"html/{file}")

    if not paths:
        raise FileNotFoundError("html файлы не найдены!")

    return sorted(paths)


def get_elements(page: str) -> list[tuple[str, str]]:
    soup = BeautifulSoup(page, "lxml")
    container = soup.find("div", class_="u-profile-container__content")
    cards = container.find_all("div", class_="card-item")

    anime = list()

    for card in cards:
        card_caption = card.find("div", class_="card-item-caption__main").text

        card_link = card.find("a", class_="cover").get("href")

        anime.append((card_caption, card_link))

    return anime


def generate_md_table(anime: list[tuple[str, str]]) -> str:
    table = "| Аниме | Ссылка |\n"
    table += "| ----- | ---- |\n"
    for anim in anime:
        table += f"| {anim[0]} | {anim[1]} |\n"

    return table


def generate_md(anime: list[tuple[str, str]]) -> str:
    output = str()

    for anim in anime:
        output += f"- [{anim[0]}]({anim[1]})\n"

    return output


def create_md_file(list_name: str, output: str) -> None:
    os.makedirs("generated", exist_ok=True)

    with open(f"generated/{list_name}.md", "w") as file:
        file.write(output)

    print(f"{list_name}.md успешно создан!")


def main() -> None:
    list_names, output_type = get_user_input()
    file_paths = get_html_paths()

    if len(list_names) != len(file_paths):
        raise FileNotFoundError(
            "Количество названий списков должно совпадать с количеством html файлов!"
        )

    for i in range(len(list_names)):
        page = read_file(file_paths[i])
        anime = get_elements(page)
        match output_type.lower():
            case "mdt":
                output = generate_md_table(anime)
            case "md":
                output = generate_md(anime)
            case _:
                raise KeyError("Неправильный тип вывода")

        create_md_file(list_names[i], output)


if __name__ == "__main__":
    main()

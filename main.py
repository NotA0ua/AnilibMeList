from bs4 import BeautifulSoup

def get_user_input() -> tuple[str, str, str]:
    file_path = input("Enter html path: ")
    print("\n")
    list_name = input("Enter the name of your list: ")
    print("\n")
    output_type = input("Enter the type of output (MDT, md): ")
    return file_path, list_name, output_type

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

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
    table =  "| Аниме | Link |\n"
    table += "| ----- | ---- |\n"
    for anim in anime:
        table += f"| {anim[0]} | {anim[1]} |\n"

    return table


def generate_md(anime: list[tuple[str, str]]) -> str:
    output = str()

    for anim in anime:
        output += f"[{anim[0]}]({anim[1]})\n"

    return output

def create_md_file(list_name: str, output: str) -> None:
    with open("generated.md", "w") as file:
        file.write(output)

    print("Successfully created generated.md")


def main() -> None:
    file_path, list_name, output_type = get_user_input()
    page = read_file(file_path)
    anime = get_elements(page)
    match output_type.lower():
        case "mdt":
            output = generate_md_table(anime)
        case "md":
            output = generate_md(anime)
        case _:
            raise KeyError("Wrong output type")

    create_md_file(list_name, output)


if __name__ == "__main__":
    main()

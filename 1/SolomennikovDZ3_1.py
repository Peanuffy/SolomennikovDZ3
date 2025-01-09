import os
import json
from bs4 import BeautifulSoup
from statistics import mean, stdev


def parse_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    category = (
        soup.find("span", text=lambda x: "Категория:" in x)
        .get_text()
        .split(":")[1]
        .strip()
    )
    title = soup.find("h1", class_="book-title").get_text().strip()
    author = soup.find("p", class_="author-p").get_text().strip()
    pages_text = (
        soup.find("span", text=lambda x: "Объем:" in x).get_text().split(":")[1].strip()
    )
    pages = int(pages_text.split()[0])
    year_text = soup.find("span", text=lambda x: "Издано в" in x).get_text()
    year = int(year_text.split()[-1])
    isbn = (
        soup.find("span", text=lambda x: "ISBN:" in x).get_text().split(":")[1].strip()
    )
    rating_text = soup.find("span", text=lambda x: "Рейтинг:" in x).get_text()
    rating = float(rating_text.split(":")[1].strip())
    views_text = soup.find("span", text=lambda x: "Просмотры:" in x).get_text()
    views = int(views_text.split(":")[1].strip())

    return {
        "category": category,
        "title": title,
        "author": author,
        "pages": pages,
        "year": year,
        "isbn": isbn,
        "rating": rating,
        "views": views,
    }


def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def calculate_statistics_data(data, field):
    values = [item[field] for item in data if field in item]
    if not values:
        return {}
    return {
        "sum": sum(values),
        "min": min(values),
        "max": max(values),
        "mean": mean(values),
        "std_dev": stdev(values) if len(values) > 1 else 0,
    }


def calculate_frequency(data, field):
    frequency = {}
    for item in data:
        if field in item:
            value = item[field]
            frequency[value] = frequency.get(value, 0) + 1
    return frequency


def main(input_folder, output_folder):
    all_data = []

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".html"):
            file_path = os.path.join(input_folder, file_name)
            all_data.append(parse_html(file_path))

    save_to_json(all_data, os.path.join(output_folder, "parsed_data.json"))

    sorted_data = sorted(all_data, key=lambda x: x.get("rating", 0), reverse=True)
    save_to_json(sorted_data, os.path.join(output_folder, "sorted_by_rating.json"))

    filtered_data = [item for item in all_data if item.get("views", 0) > 500]
    save_to_json(filtered_data, os.path.join(output_folder, "filtered_by_views.json"))

    pages_stats = calculate_statistics_data(all_data, "pages")
    save_to_json(pages_stats, os.path.join(output_folder, "pages_statistics.json"))

    category_frequency = calculate_frequency(all_data, "category")
    save_to_json(
        category_frequency, os.path.join(output_folder, "category_frequency.json")
    )


if __name__ == "__main__":
    input_folder = "C:/SolomennikovDZ3/1"
    output_folder = "C:/SolomennikovDZ3/1"

    os.makedirs(output_folder, exist_ok=True)

    main(input_folder, output_folder)

import os
import json
import xml.etree.ElementTree as ET
from statistics import mean, stdev


def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    items = []
    for clothing in root.findall("clothing"):
        item = {}
        for child in clothing:
            tag = child.tag
            text = child.text.strip()
            if tag in ["id", "price", "reviews"]:
                item[tag] = int(text)
            elif tag in ["rating"]:
                item[tag] = float(text)
            else:
                item[tag] = text
        items.append(item)
    return items


def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def calculate_statistics(data, field):
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


def count_frequency(data, field):
    frequency = {}
    for item in data:
        if field in item:
            value = item[field]
            frequency[value] = frequency.get(value, 0) + 1
    return frequency


def main(input_folder, output_folder):
    all_data = []

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".xml"):
            file_path = os.path.join(input_folder, file_name)
            all_data.extend(parse_xml(file_path))

    save_to_json(all_data, os.path.join(output_folder, "parsed_data.json"))

    sorted_data = sorted(all_data, key=lambda x: x.get("price", 0), reverse=True)
    save_to_json(sorted_data, os.path.join(output_folder, "sorted_by_price.json"))

    filtered_data = [item for item in all_data if item.get("rating", 0) > 2.5]
    save_to_json(filtered_data, os.path.join(output_folder, "filtered_by_rating.json"))

    reviews_stats = calculate_statistics_data(all_data, "reviews")
    save_to_json(reviews_stats, os.path.join(output_folder, "reviews_statistics.json"))

    color_frequency = calculate_frequency(all_data, "color")
    save_to_json(color_frequency, os.path.join(output_folder, "color_frequency.json"))


if __name__ == "__main__":
    input_folder = "C:/SolomennikovDZ3/4"
    output_folder = "C:/SolomennikovDZ3/4"

    os.makedirs(output_folder, exist_ok=True)

    main(input_folder, output_folder)

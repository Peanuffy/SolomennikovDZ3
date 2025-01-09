from bs4 import BeautifulSoup
import json


def parse_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    products = []

    product_elements = soup.find_all(class_="js-product")
    for product_element in product_elements:
        try:
            name = product_element.find(class_="js-product-name").text.strip()
            description = product_element.find(
                class_="js-store-prod-descr"
            ).text.strip()
            price_text = product_element.find(class_="js-product-price").text.strip()
            price = float(
                price_text.replace("р.", "").replace(",", "").replace(" ", "").strip()
            )
            products.append({"name": name, "description": description, "price": price})
        except AttributeError:
            continue
        except ValueError:
            continue

    return products


def sort_products_by_price(products):
    return sorted(products, key=lambda x: x["price"])


def filter_products_by_price(products, min_price=100, max_price=500):
    return [p for p in products if min_price <= p["price"] <= max_price]


def calculate_price_stats(products):
    prices = [p["price"] for p in products]
    if not prices:
        return {}

    return {
        "min_price": min(prices),
        "max_price": max(prices),
        "avg_price": sum(prices) / len(prices),
        "total_price": sum(prices),
    }


def calculate_word_frequency(products):
    word_count = {}
    for product in products:
        words = product["description"].split()
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
    return word_count


def main():
    file_path = "C:/SolomennikovDZ3/5/Интернет-магазин натуральных сыров и фермерских продуктов от Никольской Слободы. Доставка в Екатеринбург.html"
    products = parse_html_file(file_path)

    with open("products.json", "w", encoding="utf-8") as file:
        json.dump(products, file, ensure_ascii=False, indent=4)

    sorted_products = sort_products_by_price(products)
    with open("sorted_products.json", "w", encoding="utf-8") as file:
        json.dump(sorted_products, file, ensure_ascii=False, indent=4)

    filtered_products = filter_products_by_price(products, 100, 500)
    with open("filtered_products.json", "w", encoding="utf-8") as file:
        json.dump(filtered_products, file, ensure_ascii=False, indent=4)

    price_stats = calculate_price_stats(products)
    with open("price_stats.json", "w", encoding="utf-8") as file:
        json.dump(price_stats, file, ensure_ascii=False, indent=4)

    word_frequency = calculate_word_frequency(products)
    with open("word_frequency.json", "w", encoding="utf-8") as file:
        json.dump(word_frequency, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()

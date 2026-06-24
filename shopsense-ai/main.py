from products import products

def search_products(query):
    query = query.lower()

    results = []

    for product in products:
        if (
            query in product["name"].lower()
            or query in product["category"].lower()
        ):
            results.append(product)

    return results


if __name__ == "__main__":

    search = input("What are you looking for? ")

    results = search_products(search)

    if results:
        print("\nBest Matches:\n")

        for item in results:
            print(
                f"{item['name']} - "
                f"${item['price']} "
                f"({item['category']})"
            )

    else:
        print("No products found.")
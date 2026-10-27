
def calculate_total(price, quantity):
    if price < 0 or quantity < 0:
        raise ValueError("Price and quantity must be non-negative")

    return price * quantity


def main():
    total = calculate_total(100, 3)
    print(f"Total price: {total}")


if __name__ == "__main__":
    main()

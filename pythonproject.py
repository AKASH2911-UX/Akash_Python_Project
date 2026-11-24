from datetime import datetime

# Inventory dictionary: name -> {price, stock}
inventory = {
    "Rice": {"price": 50, "stock": 100},
    "Sugar": {"price": 45, "stock": 50},
    "Milk": {"price": 30, "stock": 40},
    "Oil": {"price": 150, "stock": 20},
}


def find_item(name):
    """Case-insensitive item search."""
    for key in inventory:
        if key.lower() == name.strip().lower():
            return key
    return None


def new_bill():
    cart = []  # list of items: (name, qty, price)
    print("\nItem aur quantity dalein. Bill khatam karne ke liye item name mein 'done' likhein.")
    while True:
        name = input("Item: ").strip()
        if name.lower() == "done":
            break
        key = find_item(name)
        if key is None:
            print(f"Item '{name}' not found in inventory.")
            continue
        try:
            qty = int(input("Quantity: "))
            if qty <= 0:
                raise ValueError
        except ValueError:
            print("Invalid quantity. Positive number dalein.")
            continue
        # stock me se already cart wali quantity bhi ginni hai
        in_cart = sum(q for n, q, p in cart if n == key)
        available = inventory[key]["stock"] - in_cart
        if qty > available:
            print(f"Insufficient stock for {key}. Available: {available}")
            continue
        cart.append((key, qty, inventory[key]["price"]))

    if not cart:
        print("Cart khali hai, bill nahi bana.")
        return

    # Calculations
    subtotal = sum(q * p for n, q, p in cart)
    discount = subtotal * 0.10 if subtotal >= 1000 else 0.0
    gst = (subtotal - discount) * 0.05
    total = subtotal - discount + gst

    print("\n------ BILL ------")
    for n, q, p in cart:
        print(f"{n:<8} x {q:<4} @ {p:<5} = {q * p:.2f}")
    print(f"Subtotal: {subtotal:.2f} | Discount: {discount:.2f}")
    print(f"GST (5%): {gst:.2f} | Total: Rs. {total:.2f}")

    # Stock reduce karo
    for n, q, p in cart:
        inventory[n]["stock"] -= q

    # bills.txt me append karo
    with open("bills.txt", "a") as f:
        f.write(f"\nDate: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
        for n, q, p in cart:
            f.write(f"{n} x {q} @ {p} = {q * p:.2f}\n")
        f.write(f"Subtotal: {subtotal:.2f} | Discount: {discount:.2f} | "
                f"GST (5%): {gst:.2f} | Total: Rs. {total:.2f}\n")
        f.write("-" * 40 + "\n")
    print("Bill bills.txt me save ho gaya.")


def view_stock():
    print("\n------ STOCK ------")
    print(" | ".join(f"{n}: {d['stock']}" for n, d in inventory.items()))


def main():
    while True:
        print("\n=== Grocery Store Management System ===")
        print("1. New bill")
        print("2. View stock")
        print("3. Exit")
        choice = input("Option chunein: ").strip()
        if choice == "1":
            new_bill()
        elif choice == "2":
            view_stock()
        elif choice == "3":
            print("Thank you!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
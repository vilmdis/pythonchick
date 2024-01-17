def manu():
    Inventory = {}
    while True:
        print('-' * 100)
        print(
            """
            1) View Inventory
            2) Add Item
            3) Remove Item
            4) Update Quantity
            5) Search Inventory
            6) Quit
            """
        )
        print('-' * 100)
        choose = input('Enter your choice: ')
        print('-' * 100)
        if choose == '1':
            view_inventory(Inventory)
        elif choose == '2':
            add_item(Inventory)
        elif choose == '3':
            remove_item(Inventory)
        elif choose == '4':
            update_quantity(Inventory)
        elif choose == '5':
            search_inventory(Inventory)
        elif choose == '6':
            break
        else:
            print("Invalid option. Please enter a valid option.")

def view_inventory(Inventory):
    print("Item Name\t\t\t\tDescription\t\t\t\tQuantity")
    print('-' * 100)
    for item_name, item_data in Inventory.items():
        print(f"{item_name}\t\t\t\t\t{item_data['description']}\t\t\t\t\t{item_data['quantity']}")

def add_item(Inventory):
    while True:
        item_name = input('Enter your name: ')
        print('-' * 100)
        item_description = input('Enter your description: ')
        print('-' * 100)
        item_quantity = int(input('Enter your quantity: '))
        print('-' * 100)
        Inventory[item_name] = {
            "description": item_description,
            "quantity": item_quantity
        }
        print('Item added successfully!')
        break

def remove_item(Inventory):
    while True:
        item_name = input('Enter name to delete: ')
        if item_name in Inventory:
            Inventory.pop(item_name)
            print('-' * 100)
            print(f"Item '{item_name}' has been removed from the inventory.")
            print('-' * 100)
        elif item_name == 'q':
            break
        else:
            print(f"Item '{item_name}' does not exist in the inventory.")
            print('-' * 100)


def update_quantity(Inventory):
    while True:
        item_name = input('Enter name: ')
        if item_name in Inventory:
            new_quantity = int(input("Enter new quantity: "))
            print('-' * 100)
            Inventory[item_name]["quantity"] = new_quantity
            print('Quantity has been updated!')
            print('-' * 100)
        elif item_name == 'q':
            break
        else:
            print(f"Item '{item_name}' does not exist in the inventory.")
            print('-' * 100)


def search_inventory(Inventory):
    while True:
        item_search = input('Enter name: ')
        if item_search == 'q':
            break
        for item_name, item_data in Inventory.items():
            if item_search in item_name or item_search in item_data['description']:
                print('-' * 100)
                print(f"Item: {item_name}")
                print(f"Description: {item_data['description']}")
                print(f"Quantity: {item_data['quantity']}")
                print('-' * 100)
            else:
                print(f"No items found matching the search term '{item_search}'.")
                print('-' * 100)

if __name__ == '__main__':
    manu()

# inventory_legacy.py
# Python 2.x style inventory system

import os
import sys

class InventoryManager:

    def __init__(self):
        self.inventory = {}

    def add_item(self, name, quantity):
        if self.inventory.has_key(name):
            self.inventory[name] += quantity
        else:
            self.inventory[name] = quantity
        print "Item added:", name

    def remove_item(self, name, quantity):
        if not self.inventory.has_key(name):
            print "Item not found"
            return

        if self.inventory[name] < quantity:
            print "Not enough stock"
            return

        self.inventory[name] -= quantity
        print "Item removed:", name

    def display_inventory(self):
        print "Current Inventory:"
        for key in self.inventory.keys():
            print key, ":", self.inventory[key]

    def save_to_file(self, filename):
        try:
            f = open(filename, "w")
            for key in self.inventory.keys():
                line = key + "," + str(self.inventory[key]) + "\n"
                f.write(line)
            f.close()
            print "Inventory saved"
        except Exception, e:
            print "Error saving file:", e

    def load_from_file(self, filename):
        if not os.path.exists(filename):
            print "File not found"
            return
        try:
            f = open(filename, "r")
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    self.inventory[parts[0]] = int(parts[1])
            f.close()
            print "Inventory loaded"
        except Exception, e:
            print "Error loading file:", e


def main():
    manager = InventoryManager()

    while True:
        print "\n1. Add Item"
        print "2. Remove Item"
        print "3. Display"
        print "4. Save"
        print "5. Load"
        print "6. Exit"

        choice = raw_input("Enter choice: ")

        if choice == "1":
            name = raw_input("Item name: ")
            qty = int(raw_input("Quantity: "))
            manager.add_item(name, qty)

        elif choice == "2":
            name = raw_input("Item name: ")
            qty = int(raw_input("Quantity: "))
            manager.remove_item(name, qty)

        elif choice == "3":
            manager.display_inventory()

        elif choice == "4":
            manager.save_to_file("inventory.txt")

        elif choice == "5":
            manager.load_from_file("inventory.txt")

        elif choice == "6":
            print "Exiting..."
            break

        else:
            print "Invalid option"


if __name__ == "__main__":
    main()

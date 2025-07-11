import json
from collections import deque, namedtuple

MenuItemData = namedtuple('MenuItemData', ['name', 'price'])

class MenuItem:
    def __init__(self, name, price):
        self.name = name 
        self.price = price
    
    def total_price(self):
        return self.price 

class Beverage(MenuItem):
    def __init__(self, name, price, size):
        super().__init__(name, price)
        self.size = size

class Apetizer(MenuItem):
    def __init__(self, name, price, shared):
        super().__init__(name, price)
        self.shared = shared

class MainCourse(MenuItem):
    def __init__(self, name, price, vegetarian):
        super().__init__(name, price)
        self.vegetarian = vegetarian

# FIFO (cola)
class OrderQueue:
    def __init__(self):
        self.queue = deque()

    def add_order(self, order):
        self.queue.append(order)

    def process_order(self):
        if self.queue:
            return self.queue.popleft()
        return None

class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
    
    def calculate_total(self):
        return sum(item.total_price() for item in self.items)
    
    def apply_discount(self):
        total = self.calculate_total()
        if len(self.items) > 6:
            return total * 0.8  # 20% de descuento
        return total

# Menú con JSON
class MenuManager:
    def __init__(self, filename = "menu.json"):
        self.filename = filename
        self.menu = self.load_menu()

    def load_menu(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_menu(self):
        with open(self.filename, "w") as file:
            json.dump(self.menu, file, indent=2)

    def add_item(self, category, item_data):
        if category not in self.menu:
            self.menu[category] = []
        self.menu[category].append(item_data._asdict())
        self.save_menu()

    def update_item(self, category, index, new_data):
        if category in self.menu and 0 <= index < len(self.menu[category]):
            self.menu[category][index] = new_data._asdict()
            self.save_menu()

    def delete_item(self, category, index):
        if category in self.menu and 0 <= index < len(self.menu[category]):
            del self.menu[category][index]
            self.save_menu()

# -------------------------

menu_manager = MenuManager()

item1 = MenuItemData("Coke", 1.50)
item2 = MenuItemData("Burger", 10.00)
menu_manager.add_item("Beverages", item1)
menu_manager.add_item("MainCourses", item2)

order1 = Order()
order1.add_item(Beverage("Coke", 1.50, "Medium"))
order1.add_item(MainCourse("Burger", 10.00, False))

order2 = Order()
order2.add_item(Apetizer("Wings", 6.00, True))
order2.add_item(MainCourse("Salad", 8.00, True))

order_queue = OrderQueue()
order_queue.add_order(order1)
order_queue.add_order(order2)

while True:
    next_order = order_queue.process_order()
    if not next_order:
        break
    print("Procesando orden. Total: $", next_order.apply_discount())

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QLineEdit, QSpinBox, QComboBox, QMessageBox, QGridLayout, QFormLayout, QLabel, QPushButton, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QStackedWidget
import sys

# code of William Doney aka w23012940

class Inventory:
    def __init__(self):
        self.stock = {
            "tubular steel": 105,
            "front fork": 1,
            "seats": 2,
            "lights": 30,
            "pedals": 30,
        }
        self.customizations= {
            "frame size": {
                "Small": {"steel": 10, "stock": 0},
                "Medium": {"steel": 15, "stock": 15},
                "Large": {"steel": 20, "stock": 5},
                "Extra-Large": {"steel": 25, "stock": 20},
            },
            "frame colour": {
                "Red": {"price": 10, "stock": 8},
                "Blue": {"price": 10, "stock": 14},
                "Green": {"price": 10, "stock": 30},
                "Black": {"price": 15, "stock": 25},
                "White": {"price": 15, "stock": 10},
                "Yellow": {"price": 10, "stock": 19},
                "Pink": {"price": 10, "stock": 13},
            },
            "wheel size": {
                "26-inch": {"price": 30, "stock": 3},
                "27.5-inch": {"price": 35, "stock": 52},
                "29-inch": {"price": 40, "stock": 12},
                "30-inch": {"price": 45, "stock": 19},
            },
            "gear type": {
                "Standard": {"price": 50, "stock": 16},
                "Premium": {"price": 100, "stock": 2},
            },
            "brake type": {
                "Rim": {"price": 20, "stock": 22},
                "Disc": {"price": 40, "stock": 14},
                "Drum": {"price": 30, "stock": 18},
            },
        }

        self.orders = [{
            "name": "Will",
            "email": "willdoney@icloud.com",
            "contact": "074444444",
            "address": "NE41GG",
            "frame size": "Small",
            "frame colour": "Blue",
            "wheel size": "30-inch",
            "gear type": "Premium",
            "brake type": "Drum",
            "stage": 0,
            "completed stages": []
        },
        {
            "name": "Zara",
            "email": "zara@northumbria.ac.uk",
            "contact": "0722222222",
            "address": "NE1AA",
            "frame size": "Extra-Large",
            "frame colour": "Pink",
            "wheel size": "26-inch",
            "gear type": "Standard",
            "brake type": "Rim",
            "stage": 0,
            "completed stages": []
        }]

        self.stations = {
            "frame addition": {"item": "frame", "customizations": ["frame size"]},
            "fork addition": {"item": "front fork", "customizations": []},
            "wheel addition": {"item": "set of 2 wheels", "customizations": ["wheel size"]},
            "gear addition": {"item": "gears", "customizations": ["gear type"]},
            "brake addition": {"item": "brakes", "customizations": ["brake type"]},
            "seat addition": {"item": "seats", "customizations": []},
            "light addition": {"item": "lights", "customizations": []},
            "paint addition": {"item": "paint", "customizations": ["frame colour"]},
            "pedal addition": {"item": "pedals", "customizations": []},
        }

        self.welding_stations_output = {
            "front fork welding": "front fork",
            "frame welding": "frame"
        }
        self.welding_stations_input = {
            "front fork welding": "tubular steel",
            "frame welding": "tubular steel"
        }

        self.completed = []
        self.table = QTableWidget()


class MainWindow(QMainWindow, Inventory):
    def __init__(self):
        super().__init__()
        #creating pages and initiating variables

        self.order_quantity_spinbox = None
        self.stock_dropdown = None
        self.order_dropdown = QComboBox()
        self.order_list_layout = None
        self.update_order_dropdown()
        self.frame_dropdown = QComboBox()

        self.setWindowTitle("Greener Bikes")
        self.setFixedSize(QSize(800, 600))
        self.low_stock_layout = QVBoxLayout()

        self.stack = QStackedWidget()

        self.dashboard_page = self.dashboard_page()
        self.inventory_page = self.inventory_page()
        self.order_entry_page = self.order_entry_page()

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.inventory_page)
        self.stack.addWidget(self.order_entry_page)

        self.setCentralWidget(self.stack)

    def dashboard_page(self):

        page = QWidget()
        layout = QGridLayout()

        # create buttons to other pages
        button_to_inventory = QPushButton("Go to Inventory")
        button_to_inventory.clicked.connect(lambda: self.stack.setCurrentWidget(self.inventory_page))
        button_to_inventory.setFixedSize(200, 30)
        layout.addWidget(button_to_inventory, 1, 0)

        button_to_orders = QPushButton("Go to Order Entry")
        button_to_orders.clicked.connect(lambda: self.stack.setCurrentWidget(self.order_entry_page))
        button_to_orders.setFixedSize(200, 30)
        layout.addWidget(button_to_orders,2,0)

        label = QLabel("Dashboard")
        layout.addWidget(label, 0,0)
        #welding stations

        label = QLabel("Welding Station")
        layout.addWidget(label, 3, 0)

        layout.addWidget(QLabel(f"front fork welding"), 4, 0)

        button_to_complete = QPushButton(f"complete")
        button_to_complete.setFixedSize(100, 30)

        button_to_complete.clicked.connect(lambda: self.try_complete_fork_welding_station("front fork welding"))
        layout.addWidget(button_to_complete, 5, 0)

        self.frame_dropdown = QComboBox()
        self.frame_dropdown.addItems(["Small", "Medium", "Large", "Extra-Large"])
        self.frame_dropdown.setFixedSize(200, 30)
        layout.addWidget(QLabel("Select frame size:"), 6, 0)
        layout.addWidget(self.frame_dropdown, 7, 0)

        button_to_complete_frame = QPushButton(f"complete")
        button_to_complete_frame.setFixedSize(100, 30)

        button_to_complete_frame.clicked.connect(self.try_complete_frame_welding_station)
        layout.addWidget(button_to_complete_frame, 8, 0)
        #order stations

        self.order_dropdown = QComboBox()
        self.update_order_dropdown()
        self.order_dropdown.setFixedSize(200, 30)
        layout.addWidget(QLabel("Select Order:"), 0, 1)
        layout.addWidget(self.order_dropdown, 1, 1)

        complete_stage_button = QPushButton("Complete Stage")
        complete_stage_button.clicked.connect(self.complete_selected_order_stage)
        layout.addWidget(complete_stage_button,2, 1)


        self.refresh_button = QPushButton("Show Selected Order Info")
        self.refresh_button.clicked.connect(self.update_order_info)
        layout.addWidget(self.refresh_button, 3, 1)

        self.order_list_layout = QVBoxLayout()
        self.update_order_info()
        layout.addLayout(self.order_list_layout,4,1)

        page.setLayout(layout)
        return page

    def update_order_dropdown(self):
        #adds all the names of the people who have ordered
        self.order_dropdown.clear()
        for order in self.orders:
            self.order_dropdown.addItem(order["name"])

    def update_order_info(self):
        # Clears order information and rewrites it with the updated information
        for i in reversed(range(self.order_list_layout.count())):
            widget = self.order_list_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        selected_order_name = self.order_dropdown.currentText()

        #find the selected order's information
        order = next(order for order in self.orders if order["name"] == selected_order_name)

        # shows the stages as a list
        stages = "\n".join(order["completed stages"]) if order["completed stages"] else "None"

        #get the current stage for the selected order
        current_stage = (
            list(self.stations.keys())[order["stage"]]
            if order["stage"] < len(self.stations)
            else "Completed"
        )

        #display the order information
        order_info = QLabel(f"Name: {order['name']}\nCurrent Stage: {current_stage}\nCompleted Stages:\n{stages}")
        self.order_list_layout.addWidget(order_info)
        self.refresh_inventory()

    def complete_selected_order_stage(self):
        selected_order_name = self.order_dropdown.currentText()
        selected_order = next(order for order in self.orders if order["name"] == selected_order_name)

        # check if the order is complete and shows a pop up for delivery
        if selected_order["stage"] >= len(self.stations) - 1:
            self.completed.append(selected_order)
            self.orders.remove(selected_order)
            self.update_order_dropdown()

            self.offer_delivery(selected_order)

            QMessageBox.information(self, "Completed", f"Order for {selected_order_name} has been fully completed!")
            return

        # get the current stage and its details
        current_stage_name = list(self.stations.keys())[selected_order["stage"]]
        stage_info = self.stations[current_stage_name]
        item_name = stage_info["item"]
        next_stage = list(self.stations.keys())[selected_order["stage"]]

        # Check stock for items
        if item_name in self.stock:
            if self.stock[item_name] <= 0:
                QMessageBox.warning(self, "Error", f"Insufficient stock for {item_name}.")
                return

            self.stock[item_name] -= 1
            selected_order["completed stages"].append(current_stage_name)
            selected_order["stage"] += 1
            QMessageBox.information(self, "Success",
                                        f"Stage '{current_stage_name}' completed(using 1 {item_name})! Next stage: {next_stage}.")

        # Check stock for the order and it's customization
        for customization_key in stage_info["customizations"]:
            current_customization = selected_order[customization_key]
            if current_customization:
                category_items = self.customizations.get(customization_key)
                if category_items and current_customization in category_items:
                    if category_items[current_customization]["stock"] > 0:
                        category_items[current_customization]["stock"] -= 1
                        selected_order["completed stages"].append(current_stage_name)
                        selected_order["stage"] += 1
                        QMessageBox.information(self, "Success",
                                                f"Stage '{current_stage_name}' completed (using 1 {current_customization} - {item_name})! Next stage: {next_stage}.")
                    else:
                        QMessageBox.warning(self, "Error", f"Insufficient stock for {current_customization} - {item_name}.")
                        return
                else:
                    QMessageBox.warning(self, "Error", f"Invalid customization: {current_customization}.")
                    return

        self.update_order_info()
        self.refresh_inventory()

    def offer_delivery(self, completed_order):
        customer_name = completed_order["name"]
        response = QMessageBox.question(
            self,
            "Delivery Confirmation",
            f"The order for {customer_name} is complete. Would you like to send it for delivery?",
            QMessageBox.Yes | QMessageBox.No
        )
        if response == QMessageBox.Yes:
            QMessageBox.information(self, "Delivery", f"The bike for {customer_name} has been sent for delivery!")
        else:
            QMessageBox.information(self, "Delivery", f"The bike for {customer_name} has been marked as ready for pickup.")

    def try_complete_station(self,station, item):
        if self.stock[item] > 0:
            self.complete_station(station, item, 5)
        if self.stock[item]<=3:
            self.show_low_stock_alert(item)

    def try_complete_fork_welding_station(self, station):

        input_item = self.welding_stations_input.get(station)

        if self.stock[input_item] > 4:
            self.complete_fork_welding_station(station,5,1)
        elif self.stock[input_item] <= 3:
            self.show_low_stock_alert(input_item)

    def try_complete_frame_welding_station(self):

        station = self.frame_dropdown.currentText()
        input = self.customizations["frame size"][station]["steel"]

        input_item = "tubular steel"
        required_steel = self.customizations["frame size"][station]["steel"]

        if self.stock[input_item] >= required_steel:
            self.complete_frame_welding_station(station,input,1)
        else:
            self.refresh_inventory()
            alert = QMessageBox()
            alert.setIcon(QMessageBox.Warning)
            alert.setWindowTitle("Low Stock Alert")
            alert.setText(f"Stock for '{input_item}' is now {self.stock[input_item]}. order more to complete this station.")
            alert.exec()
    def complete_station(self, station, item, quantity):
        # take away from the items stock
        if item in self.stock and station not in self.completed:
            self.stock[item] -= quantity
            self.refresh_inventory()


    def complete_fork_welding_station(self, station, input_quantity, output_quantity):
        #take away from the forks stock
        input_item = self.welding_stations_input.get(station)
        output_item = self.welding_stations_output.get(station)

        if input_item in self.stock and output_item in self.stock:
            self.stock[input_item] -= input_quantity
            self.stock[output_item] += output_quantity
            self.refresh_inventory()
            self.welded_stock_alert(self.welding_stations_output.get(station), 1, input_quantity)

    def complete_frame_welding_station(self, size, input_quantity, output_quantity):
        #removes the appropriate tubular steel from the stock and adding the appropriate frame to stock
        input_item = "tubular steel"
        output_item = size
        frame_sizes = self.customizations.get("frame size", {})
        customization = frame_sizes.get(output_item, {})
        required_quantity = customization.get("steel", input_quantity)

        current_stock = self.stock.get(input_item, 0)

        if current_stock >= required_quantity:
            self.stock[input_item] -= required_quantity

            if output_item in frame_sizes:
                frame_sizes[output_item]["stock"] = frame_sizes[output_item].get("stock", 0) + output_quantity
            self.welded_stock_alert(f"{size} frame", 1, input_quantity)
            self.refresh_inventory()


    def show_low_stock_alert(self, item):

        self.refresh_inventory()
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Warning)
        alert.setWindowTitle("Low Stock Alert")
        if self.stock[item] >= 0:
            alert.setText(f"Stock for '{item}' is now {self.stock[item]}. Please order or weld more to complete this station.")
        else:
            alert.setText(f"Stock for {item} is now 0. Order more so the next order can be fulfilled")
        alert.exec()

    def replenished_stock_alert(self, item, quantity):
        self.refresh_inventory()
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Warning)
        alert.setWindowTitle("Items ordered")
        alert.setText(f"Ordered {quantity} {item}")
        alert.exec()

    def welded_stock_alert(self, item, quantity, input):
        self.refresh_inventory()
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Warning)
        alert.setWindowTitle("Items ordered")
        alert.setText(f"Welded {quantity} {item} using {input} tubular steel")
        alert.exec()

    def alert(self, message):
        self.refresh_inventory()
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Warning)
        alert.setWindowTitle("Alert")
        alert.setText(f"{message}")
        alert.exec()

    def update_table(self):
        # setting the total rows of stock
        total_rows = len(self.stock)
        for category, options in self.customizations.items():
            for option, details in options.items():
                total_rows += 1

        self.table.setRowCount(total_rows)

        row = 0
        # adding all the items in stock and customizations to the table

        for row, (Item, Quantity) in enumerate(self.stock.items()):
            self.table.setItem(row, 0, QTableWidgetItem(str(Item)))
            self.table.setItem(row, 1, QTableWidgetItem(str(Quantity)))
            row += 1

        for category, options in self.customizations.items():
            for option, details in options.items():
                self.table.setItem(row, 0, QTableWidgetItem(f"{category}: {option}"))
                self.table.setItem(row, 1, QTableWidgetItem(str(details.get("stock", 0))))
                row += 1

    def inventory_page(self):

        page = QWidget()
        layout = QGridLayout()

        label = QLabel("Inventory Page")
        layout.addWidget(label, 0, 0)

        button_to_dashboard = QPushButton("Back to Dashboard")
        button_to_dashboard.clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboard_page))
        button_to_dashboard.setFixedSize(200, 30)
        layout.addWidget(button_to_dashboard, 1, 0)

        # add table with the information on materials and quantity
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Item", "Quantity"])

        self.update_table()

        self.table.setFixedWidth(250)
        self.table.setColumnWidth(0, 130)
        self.table.setColumnWidth(1, 75)
        layout.addWidget(self.table, 2, 0, 5 ,0)

        label_low_stock = QLabel("Low stock (< 4)")
        layout.addWidget(label_low_stock, 1, 1)

        self.low_stock_layout = QVBoxLayout()
        layout.addLayout(self.low_stock_layout, 2, 1)

        self.update_low_stock_items()

        label = QLabel("Order stock")
        layout.addWidget(label, 3, 1)

        self.stock_dropdown = QComboBox()
        self.order_quantity_spinbox = QSpinBox()
        #adding stock items and customization tiems

        dropdown_items = list(self.stock.keys())

        for customization_type, options in self.customizations.items():
            for option_name, details in options.items():
                dropdown_items.append(f"{option_name} - {customization_type}")

        self.stock_dropdown.addItems(dropdown_items)
        layout.addWidget(self.stock_dropdown, 4, 1)

        #box for selecting order quantity
        self.order_quantity_spinbox.setRange(1, 100)
        self.order_quantity_spinbox.setValue(10)
        layout.addWidget(self.order_quantity_spinbox, 5, 1)

        # Order button
        button_order_stock = QPushButton("Order Selected Stock")
        button_order_stock.clicked.connect(self.order_selected_stock)
        button_order_stock.setFixedSize(200, 30)
        layout.addWidget(button_order_stock, 6, 1)

        page.setLayout(layout)

        return page

    def order_selected_stock(self):
        # add the total stock ordered to the stock
        selected_item = self.stock_dropdown.currentText()

        if not selected_item:
            self.alert("No item selection in dropdown")
            return

        order_quantity = self.order_quantity_spinbox.value()
        if selected_item in self.stock:
            self.stock[selected_item] += order_quantity
            self.update_table()
            self.refresh_inventory()
        else:
            first_word = selected_item.split()[0]
            for category, items in self.customizations.items():
                if first_word in items:
                    self.customizations[category][first_word]["stock"] += order_quantity
                    self.update_table()
                    self.refresh_inventory()

        self.refresh_inventory()
        self.replenished_stock_alert(selected_item, order_quantity)


    def update_low_stock_items(self):

        cat = 0

        for i in reversed(range(self.low_stock_layout.count())):
            widget = self.low_stock_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

            # add the low stock item and either tell them to weld more or order more
        for item, quantity in self.stock.items():
            if quantity < 4:
                if item == "front fork":
                    label = QLabel(f"Low Stock: {item} (Quantity: {quantity})")
                    self.low_stock_layout.addWidget(label)
                    label = QLabel(f"Weld more using tubular steel")
                    self.low_stock_layout.addWidget(label)
                    cat += 1
                else:
                    label = QLabel(f"Low Stock: {item} (Quantity: {quantity})")
                    button_order_more = QPushButton("Emergency Order 10 More")
                    button_order_more.setFixedSize(150, 30)
                    button_order_more.clicked.connect(lambda _, i=item:self.order_more_stock(i))

                    self.low_stock_layout.addWidget(label)
                    self.low_stock_layout.addWidget(button_order_more)

                    cat+=1

        for category, options in self.customizations.items():
            for option, details in options.items():
                stock = details.get("stock", 0)
                if stock < 4:
                    if category == "frame size":
                        label = QLabel(f"Low Stock: {category} - {option} (Quantity: {stock})")
                        self.low_stock_layout.addWidget(label)
                        label = QLabel(f"Weld more using tubular steel")
                        self.low_stock_layout.addWidget(label)
                        cat += 1
                    else:
                        label = QLabel(f"Low Stock: {category} - {option} (Quantity: {stock})")
                        button_order_more = QPushButton("Emergency Order 10 More")
                        button_order_more.setFixedSize(150, 30)

                        # Pass category and option to the order method
                        button_order_more.clicked.connect(lambda _, c=category, o=option: self.order_more_customization_stock(c, o))

                        self.low_stock_layout.addWidget(label)
                        self.low_stock_layout.addWidget(button_order_more)
                        cat += 1

        if not cat:
            label = QLabel(f"No Low Stock!")
            self.low_stock_layout.addWidget(label)

    def order_more_stock(self, item):
        # Add 10 to the stock
        if item in self.stock:
            self.stock[item] += 10
            self.update_table()
            self.refresh_inventory()
            self.replenished_stock_alert(item, 10)

    def order_more_customization_stock(self, category, option):
        # Add 10 to the stock
        self.customizations[category][option]["stock"] += 10
        self.update_table()
        self.refresh_inventory()
        self.replenished_stock_alert(f"{category} - {option}", 10)

    def refresh_inventory(self):
        #updates items in the inventory
        self.update_table()
        self.update_low_stock_items()

    def order_entry_page(self):
        page = QWidget()
        layout = QFormLayout()

        label = QLabel("Order Entry Page")
        layout.addRow(label)

        # options to add persoanl information
        self.name_input = QLineEdit()
        layout.addRow("Name:", self.name_input)

        self.email_input = QLineEdit()
        layout.addRow("Email:", self.email_input)

        self.contact_input = QLineEdit()
        layout.addRow("Contact Number:", self.contact_input)

        self.address_input = QLineEdit()
        layout.addRow("address:", self.address_input)


        # bike customization options
        self.frame_size_dropdown = QComboBox()
        self.frame_size_dropdown.addItems(self.customizations["frame size"])
        layout.addRow("Frame Size:", self.frame_size_dropdown)

        self.frame_colour_dropdown = QComboBox()
        self.frame_colour_dropdown.addItems(self.customizations["frame colour"])
        layout.addRow("Frame Colour:", self.frame_colour_dropdown)

        self.wheel_size_dropdown = QComboBox()
        self.wheel_size_dropdown.addItems(self.customizations["wheel size"])
        layout.addRow("Wheel Size:", self.wheel_size_dropdown)

        self.gears_dropdown = QComboBox()
        self.gears_dropdown.addItems(self.customizations["gear type"])
        layout.addRow("Gears:", self.gears_dropdown)

        self.brakes_dropdown = QComboBox()
        self.brakes_dropdown.addItems(self.customizations["brake type"])
        layout.addRow("Brakes:", self.brakes_dropdown)

        # one button to submit and save the order and another to create a popup to show all the orders
        submit_button = QPushButton("Submit Order")
        submit_button.clicked.connect(self.store_order)

        view_orders_button = QPushButton("View Orders")
        view_orders_button.clicked.connect(self.view_orders)

        view_completed_orders_button = QPushButton("View Completed Orders")
        view_completed_orders_button.clicked.connect(self.view_completed_orders)

        layout.addRow(submit_button)
        layout.addRow(view_orders_button)
        layout.addRow(view_completed_orders_button)

        button_to_dashboard = QPushButton("Back to Dashboard")
        button_to_dashboard.clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboard_page))
        layout.addRow(button_to_dashboard)

        page.setLayout(layout)
        return page

    def store_order(self):
        #use the inputs to gather all the informationa and store it about the order
        name = self.name_input.text()
        email = self.email_input.text()
        contact = self.contact_input.text()
        address = self.address_input.text()

        frame_size = self.frame_size_dropdown.currentText()
        frame_colour = self.frame_colour_dropdown.currentText()
        wheel_size = self.wheel_size_dropdown.currentText()
        gears = self.gears_dropdown.currentText()
        brakes = self.brakes_dropdown.currentText()

        if not name or not email or not contact:
            self.alert("Please fill in all personal information.")
            return

        #check if the name is a string
        if not isinstance(name, str):
            self.alert("Invalid name, it must only include letters.")
            return

            # Check if email includes '@'
        if not isinstance(email, str) or "@" not in email:
            self.alert("Invalid email. It should include '@'.")
            return

            # Check if contact is a number
        if not contact.isdigit():
            self.alert("Invalid contact, it should be a valid number.")
            return


        # Store the order in the orders list
        order = {
            "name": name,
            "email": email,
            "contact": contact,
            "address": address,
            "frame size": frame_size,
            "frame colour": frame_colour,
            "wheel size": wheel_size,
            "gear type": gears,
            "brake type": brakes,
            "stage": 0,
            "completed stages": []
        }

        self.orders.append(order)

        #clear fields after storing the most recent order
        self.name_input.clear()
        self.email_input.clear()
        self.contact_input.clear()
        self.address_input.clear()
        self.frame_size_dropdown.setCurrentIndex(0)
        self.frame_colour_dropdown.setCurrentIndex(0)
        self.wheel_size_dropdown.setCurrentIndex(0)
        self.gears_dropdown.setCurrentIndex(0)
        self.brakes_dropdown.setCurrentIndex(0)
        self.update_order_dropdown()

        self.alert("Order submitted successfully!")

    def view_orders(self):
        # display all orders in a message box
        if not self.orders:
            self.alert("No orders have been placed yet.")
            return

        orders_text = "\n\n".join(
            f"Customer: {order['name']}\n"
            f"Email: {order['email']}\n"
            f"Contact: {order['contact']}\n"
            f"address:{order['address']}\n"
            f"Frame Size: {order['frame size']}\n"
            f"Frame Colour: {order['frame colour']}\n"
            f"Wheel Size: {order['wheel size']}\n"
            f"Gears: {order['gear type']}\n"
            f"Brakes: {order['brake type']}"
            for order in self.orders
        )

        message_box = QMessageBox()
        message_box.setWindowTitle("Customer Orders")
        message_box.setText(orders_text)
        message_box.exec()

    def view_completed_orders(self):
        # display all orders in a message box
        if not self.completed:
            self.alert("There are currently no complete orders")
            return

        orders_text = "\n\n".join(
            f"Customer: {order['name']}\n"
            f"Email: {order['email']}\n"
            f"Contact: {order['contact']}\n"
            f"address:{order['address']}\n"
            f"Frame Size: {order['frame size']}\n"
            f"Frame Colour: {order['frame colour']}\n"
            f"Wheel Size: {order['wheel size']}\n"
            f"Gears: {order['gear type']}\n"
            f"Brakes: {order['brake type']}"
            for order in self.orders
        )

        message_box = QMessageBox()
        message_box.setWindowTitle("Customer Orders")
        message_box.setText(orders_text)
        message_box.exec()







app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
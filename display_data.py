class MenuItem:
    def __init__(self, label, data_type=None, action=None, sub_menu=None, value=None, options=None):
        self.label = label
        self.data_type = data_type  # Could be 'int', 'float', 'text', 'toggle', etc.
        self.action = action
        self.sub_menu = sub_menu or []
        self.value = value
        self.options = options if options else []
        self.current_option_index = 0 if data_type == "toggle" else None

    def is_sub_menu(self):
        return bool(self.sub_menu)

    def is_action(self):
        return self.action is not None

    def is_value(self):
        return self.data_type is not None

    def is_text_input(self):
        return self.data_type == "text"

    def is_int_input(self):
        return self.data_type == "int"

    def is_toggle(self):
        return self.data_type == "toggle" and bool(self.options)

    def update_value(self, new_value):
        self.value = new_value

    def toggle_option(self):
        if self.is_toggle():
            self.current_option_index = (self.current_option_index + 1) % len(self.options)
            self.value = self.options[self.current_option_index]

    def select_toggle_option(self, index):
        if self.is_toggle() and 0 <= index < len(self.options):
            self.current_option_index = index
            self.value = self.options[index]

class DisplayBuffer:
    def __init__(self, rows=None):
        self.buffer = []
        self.cursor_position = 0
        self.rows = list(range(0,len(self.buffer))) if rows == None else list(range(0,rows))
        self.direction=None
        self.total_items=0

    def update_buffer(self, menu_items, cursor_position, total_items):
        self.cursor_position=cursor_position
        self.total_items=total_items
        self.buffer = []
        for i, item in enumerate(menu_items):
            if i == cursor_position:
                self.buffer.append(f"> {item.label}")
                if item.is_value() and item.value is not None:
                    self.buffer.append(f"   Value: {item.value}")
            else:
                self.buffer.append(f"  {item.label}")

    def display(self):
        print("\nDisplay Buffer:")
        for line in self.buffer:
            print(line)
        print("\nEnd of Buffer\n")
    
    def display_calsci(self, direction):
        if direction=="down":
            if self.cursor_position>self.rows[-1]:
                # print(self.rows)
                self.rows=self.rows[::-1]
                self.rows.pop()
                # print(self.rows)
                self.rows=self.rows[::-1]
                self.rows.append(self.cursor_position)
            elif self.cursor_position==0:
                self.rows=list(range(0,len(self.rows)))
            print(self.rows, self.cursor_position)
            return 0
        

        if direction=="up" and self.cursor_position<self.rows[0]:
            if self.cursor_position<self.rows[0]:
                self.rows.pop()
                self.rows=self.rows[::-1]
                self.rows.append(self.cursor_position)
                self.rows=self.rows[::-1]
                print(self.rows, self.cursor_position)
                return 0
            # if self.cursor_position > self.rows[-1]:
            #     self.rows=list(range(len(self.buffer)-len(self.rows), len(self.buffer)))

                # self.rows=self.rows[len(self.buffer)-len(self.rows):len(self.buffer)]
        if self.cursor_position > self.rows[-1] and direction=="up":
        # if self.cursor_position == self.total_items and direction=="up":
            self.rows=list(range(self.total_items-len(self.rows), self.total_items))
            # self.rows=list(range(len(self.buffer)-len(self.rows), len(self.buffer)))

            print(self.rows, self.cursor_position)
            return 0
        # if direction=="up":
        #     self.rows=list(range(self.total_items-len(self.rows), self.total_items))
        #     print(self.rows, self.cursor_position)
        #     return 0
        if self.rows==list(range(0,len(self.rows))) and self.cursor_position==self.total_items-1:

            self.rows=list(range(self.total_items-len(self.rows), self.total_items))
            return 0
        print(self.rows, self.cursor_position)
        # menu.move_cursor_up()
        # from display_data import *
        # menu.select_item()


class Menu:
    def __init__(self, rows=2):
        self.menu_stack = []
        self.current_menu = []
        self.cursor_position = 0
        # self.display_buffer = DisplayBuffer(rows=rows)
        self.direction=None
        self.total_items=0
        self.no_rows=rows
        self.display_buffer = DisplayBuffer(rows=self.no_rows)

    def add_menu_item(self, menu_item):
        self.current_menu.append(menu_item)
        self.total_items+=1

    def enter_sub_menu(self):
        if self.current_menu[self.cursor_position].is_sub_menu():
            self.menu_stack.append((self.current_menu, self.cursor_position))
            self.current_menu = self.current_menu[self.cursor_position].sub_menu
            self.cursor_position = 0
            self.total_items=len(self.current_menu)
            # if len(self.current_menu)<=self.no_rows:
            #     self.no_rows=len(self.current_menu)
            #     self.display_buffer = DisplayBuffer(rows=self.no_rows)

            self.update_display()

    def go_back(self):
        if self.menu_stack:
            self.current_menu, self.cursor_position = self.menu_stack.pop()
            self.total_items=len(self.current_menu)
            self.update_display()

    def move_cursor_down(self):
        if self.cursor_position < len(self.current_menu) - 1:
            self.cursor_position += 1
            # self.direction="down"
        else:
            self.cursor_position = 0  # Wrap to the top
        self.direction="down"
        self.update_display()

    def move_cursor_up(self):
        if self.cursor_position > 0:
            self.cursor_position -= 1
            # self.direction="up"
        else:
            self.cursor_position = len(self.current_menu) - 1  # Wrap to the bottom
        self.direction="up"

        self.update_display()

    def select_item(self):
        current_item = self.current_menu[self.cursor_position]
        if current_item.is_action():
            current_item.action()
        elif current_item.is_sub_menu():
            self.enter_sub_menu()
        elif current_item.is_text_input() or current_item.is_int_input():
            new_value = input(f"Enter new value for {current_item.label}: ")
            if current_item.is_int_input():
                try:
                    new_value = int(new_value)
                except ValueError:
                    print("Invalid input, please enter an integer.")
                    return
            current_item.update_value(new_value)
            self.update_display()
        elif current_item.is_toggle():
            # self.total_items=
            self.enter_sub_menu()
        else:
            if self.menu_stack and self.menu_stack[-1]:  # Check if menu_stack is non-empty
                parent_menu, parent_cursor = self.menu_stack[-1]
                if parent_menu[parent_cursor].is_toggle():
                    parent_menu[parent_cursor].select_toggle_option(self.cursor_position)
                    self.go_back()

    def update_display(self):
        self.display_buffer.update_buffer(self.current_menu, self.cursor_position, total_items=self.total_items)
        self.display_buffer.display()
        self.display_buffer.display_calsci(self.direction)


# Example usage
menu = Menu(rows=3)
menu.add_menu_item(MenuItem("Item 1", sub_menu=[MenuItem("Subitem 1", sub_menu=[MenuItem("deep1"), MenuItem("deep2")]), MenuItem("Subitem 2")]))
menu.add_menu_item(MenuItem("Item 2", data_type="int", value=42))
menu.add_menu_item(MenuItem("Text Input Item 3", data_type="text"))

toggle_sub_menu = [MenuItem(f"Option {i+1}") for i in range(5)]
toggle_item = MenuItem("Toggle Option 4", data_type="toggle", value="Option 1", options=["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"], sub_menu=toggle_sub_menu)
menu.add_menu_item(toggle_item)

menu.add_menu_item(MenuItem("Item 5", action=lambda: print("Action performed")))
menu.add_menu_item(MenuItem("Item 6", data_type="int", value=42))
menu.add_menu_item(MenuItem("Item 7", data_type="int", value=42))

menu.update_display()

# Simulate user interaction
# menu.move_cursor_down()  # Move to Item 2
# menu.select_item()       # Edit the integer value of Item 2
# menu.move_cursor_down()  # Move to Text Input Item
# menu.select_item()       # Input text for Text Input Item
# menu.move_cursor_down()  # Move to Toggle Option
# menu.select_item()       # Enter the toggle submenu to select an option
# menu.move_cursor_down()  # Navigate within the toggle options
# menu.select_item()       # Select an option within the toggle submenu
# menu.go_back()           # Go back to the main menu
# menu.move_cursor_down()  # Move to Item 3
# menu.select_item()       # Perform the action for Item 3
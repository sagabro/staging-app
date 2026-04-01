import tkinter as tk
from typing import Any

import databaselogic as db
from tkinter import simpledialog, messagebox

tables = {}

class Application(tk.Tk):
    tables = {}
    def __init__(self):
        super().__init__()
        self.app = None
        self.item = None
        self.title("Real-Time Drawing")

        self.draw_mode = None
        self.current_condition = None
        self.selected_item = None
        self.last_x ,self.start_y, self.start_x,self.last_y = 0,0,0,0
        self.current_shape = None

        self.mode_handlers = {
            "move": self._handle_move,
            "condition": self._handle_condition,
            "delete": self._handle_delete,
            "select": self._handle_select,
            "seating": self._handle_seating,
            "rectangle": self._handle_rectangle,
            "oval": self._handle_oval,
        }

        self.list_section_frame = tk.Frame(self)
        self.list_section_frame.pack(side=tk.LEFT, fill="y", padx=5, pady=5)

        entry = tk.Entry(self.list_section_frame) # Parent is now the frame
        entry.pack(fill="x")
        entry.config(font=("arial",20))

        list_box = tk.Listbox(self.list_section_frame) # Parent is now the frame
        list_box.pack(fill="y", expand=True)

        def add_to_list():
            server_name = entry.get().strip().lower()

            if server_name:
                try:
                    Server(server_name=server_name)
                    list_box.insert(tk.END, server_name)
                    list_box.config(font=("arial",20))
                except ValueError as e:
                    print(e)
                    pass
                finally:
                    entry.delete(0, tk.END)

        def delete_list():
            if list_box.curselection():
                cursor = list_box.curselection()
                list_box.delete(cursor)

        delete_btn = tk.Button(self.list_section_frame, text="delete form list", command=delete_list)
        delete_btn.pack(fill="x")
        enter_btn = tk.Button(self.list_section_frame, text="Add", command=add_to_list)
        enter_btn.pack(fill="x")

        self.menu_visible = True
        self.toggle_btn = tk.Button(self, text="Toggle Menu", command=self.toggle_menu, bg="lightgrey")
        self.toggle_btn.pack(side=tk.TOP)

        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack()

        mode_frame = tk.Frame(self.btn_frame)
        mode_frame.pack()
        for mode in ["Rectangle", "Oval", "Move", "Delete","select", "seating","condition"]:
            tk.Button(mode_frame, text=mode,command=lambda m=mode.lower(): self.set_mode(m),bg='lightgrey').pack(side=tk.LEFT)

        color_frame = tk.Frame(self.btn_frame)
        color_frame.pack(pady=5)
        condition = [("sat", "red"), ("cleaning","gold"), ("clean", "green",), ("check", "orange")]

        for condition, color in condition:
            tk.Button(color_frame, bg='lightgrey', text=condition, fg=color, command=lambda c=color: self.set_condition(c)).pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self, bg="white", width=400, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-1>", lambda e: select_shape(e), add="+")

    def set_condition(self, color):
        self.current_condition = color
        self.draw_mode = "condition"

    def _handle_condition(self, event):
        self.current_shape = None
        items = self.canvas.find_closest(event.x, event.y)  # Find closest shape to click
        if items:
            item_id = items[0]
            self.canvas.itemconfig(item_id, fill=self.current_condition, outline="black")
        
            if item_id in self.tables:
                self.tables[item_id]["condition"] = self.current_condition
            else:
                self.tables[item_id] = {"condition": self.current_condition}

    def toggle_menu(self):
        if self.menu_visible:
            self.btn_frame.pack_forget()
            self.toggle_btn.config(text="Show Menu")
            self.menu_visible = False
        else:
            self.btn_frame.pack(before=self.canvas, pady=2)
            self.toggle_btn.config(text="Hide Menu")
            self.menu_visible = True

    def set_mode(self, mode):
        self.draw_mode = mode
        self.current_shape = None
        self.selected_item = None

    def on_press(self, event):
        handler = self.mode_handlers.get(self.draw_mode)
        if handler:
            handler(event)  # Calls _handle_condition(event)
        self.last_x, self.last_y = event.x, event.y

    def _handle_move(self, event):
        items = self.canvas.find_closest(event.x, event.y)
        if items:
            item_id = items[0]
            if item_id in self.tables:
                self.selected_item = item_id
            else:
                for shape_id, data in self.tables.items():
                    if data.get("label_id") == item_id:
                        self.selected_item = shape_id
                        break
                else:
                    self.selected_item = item_id
                    self.last_x, self.last_y = event.x, event.y

    def _handle_delete(self, event):
        self.current_shape = None
        items = self.canvas.find_closest(event.x, event.y)
        if items:
            item_id = items[0]
            self.canvas.delete(item_id)
            self.tables.pop(item_id, None)

    def _handle_select(self, event):
        self.current_shape = None

    def _handle_seating(self, event):
        self.current_shape = None
        items = self.canvas.find_closest(event.x, event.y)
        if items:
            item_id = items[0]
            table_size = pop_up(self, simpledialog.askinteger, "Table size", "how many:") or 0
            if item_id in self.tables:
                self.tables[item_id]["table_size"] = table_size
            print(f"Table {item_id} now seats {table_size}")

    def _handle_rectangle(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.current_shape = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline="black", fill=self.current_condition,
        )

    def _handle_oval(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.current_shape = self.canvas.create_oval(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline="black", fill=self.current_condition,
        )

    def on_release(self,event):
        if self.draw_mode in ("rectangle", "oval") and self.current_shape:
            table_size = pop_up(self, simpledialog.askinteger, "Table size", "Enter table size:") or 0
            self.tables[self.current_shape] = {"table_size": table_size}

            shape_coords = self.canvas.coords(self.current_shape)
            text_x = (shape_coords[0] + shape_coords[2]) / 2
            text_y = (shape_coords[1] + shape_coords[3]) / 2
            label_id = self.canvas.create_text(text_x, text_y,
                text=str(table_size),
                fill="black",
                font=("Arial", 12),
                tags=("shape","1"))

            group_tag = f"group_{self.current_shape}"
            self.canvas.addtag_withtag(group_tag, self.current_shape)
            self.canvas.addtag_withtag(group_tag, label_id)

            self.current_shape = None
            print(self.tables)

            self.tables[self.current_shape] = {
                "table_id": self.current_shape,
                "coords": shape_coords,
                "item_type": self.draw_mode,
                "condition": self.current_condition,
                "table_size": table_size,
                "label_id": label_id,
                "group_tag": group_tag,
            }
            self.current_shape = None
            print(self.tables)

    def on_drag(self, event):
        if self.draw_mode in ("rectangle", "oval"):
            if self.current_shape:
                self.canvas.coords(self.current_shape, self.start_x, self.start_y, event.x, event.y)
        elif self.draw_mode == "move":
            dx, dy = event.x - self.last_x, event.y - self.last_y
            group_tag = self.tables.get(self.selected_item, {}).get("group_tag")
            if group_tag:
                self.canvas.move(group_tag, dx, dy)
            self.last_x, self.last_y = event.x, event.y
app = Application()

def select_shape(event):
    if app.draw_mode == "select":
        items = app.canvas.find_closest(event.x, event.y)
        if items:
            if app.selected_item:
                app.canvas.itemconfig(app.selected_item, outline="black", width=1)
            app.selected_item = items[0]
            app.canvas.itemconfig(app.selected_item, outline="lightblue", width=3) 
            print(f"Selected shape ID: {app.selected_item}")
        else:
            if app.selected_item == "lightblue":
                app.canvas.itemconfig(app.selected_item, outline="black", width=1)
                app.selected_item = None
                print("Deselected shape")
def pop_up(app, dialog_callable, *args, **kwargs):
    x, y = app.winfo_rootx(), app.winfo_rooty()
    window = tk.Toplevel(app)
    window.overrideredirect(True)
    window.geometry(f"+{x}+{y}")

    window.update_idletasks()
    try:
        kwargs.setdefault("parent", window)
        return dialog_callable(*args, **kwargs)
    finally:
        window.destroy()

class Server:
    server_dict = {}

    def __init__(self, server_name: str):
        rotation = pop_up(app, simpledialog.askinteger, "Rotation", "order in rotation:") or 0
        section = pop_up(app, simpledialog.askstring, "Section", "Enter section name:") or None

        self.server_name = server_name

        Server.server_dict[server_name] = {
            "name": server_name,
            "rotation": rotation,
            "section_name": section,
            "amount_of_tables": 0
        }
        print(Server.server_dict)

if __name__ == "__main__":
    #db.delete_database("sections")
    #db.create_datatable()
    #db.delete_servers("")
    #server.get_rotation()
    app.mainloop()
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
        self.current_color = None
        self.selected_item = None
        self.last_x ,self.start_y, self.start_x,self.last_y = 0,0,0,0
        self.current_shape = None

        self.list_section_frame = tk.Frame(self)
        self.list_section_frame.pack(side=tk.LEFT, fill="y", padx=5, pady=5)

        entry = tk.Entry(self.list_section_frame) # Parent is now the frame
        entry.pack(fill="x")

        list_box = tk.Listbox(self.list_section_frame) # Parent is now the frame
        list_box.pack(fill="y", expand=True)

        def add_to_list():
            server_name = entry.get().strip().lower()
            if server_name:
                try:
                    Server(server_name=server_name)
                    list_box.insert(tk.END, server_name)
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

        # Shorter way to create mode buttons
        mode_frame = tk.Frame(self.btn_frame)
        mode_frame.pack()
        for mode in ["Rectangle", "Oval", "Move", "Paint", "Delete","select", "seating",]:
            tk.Button(mode_frame, text=mode,command=lambda m=mode.lower(): self.set_mode(m),bg='lightgrey').pack(side=tk.LEFT)

        # Shorter way to create color buttons
        color_frame = tk.Frame(self.btn_frame)
        color_frame.pack(pady=5)
        colors = [("Red", "red"), ("yellow","yellow"), ("Green", "green",), ("orange", "orange")]

        for text, color in colors:
            tk.Button(color_frame,bg='lightgrey', text=text, fg=color, command=lambda c=color: self.set_color(c)).pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self, bg="white", width=400, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-1>", lambda e: select_shape(e), add="+")

    def set_color(self, color):
        self.current_color = color

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
        if self.draw_mode == "move":
            self.current_shape = None
            items = self.canvas.find_closest(event.x, event.y)
            if items:
                self.selected_item = items[0]
                self.last_x, self.last_y = event.x, event.y

        elif self.draw_mode == "paint":
            self.current_shape = None
            items = self.canvas.find_closest(event.x, event.y)
            if items:
                self.canvas.itemconfig(items[0], fill=self.current_color, outline="black")
                tables.setdefault(items[0], {"color": self.current_color})


        elif self.draw_mode == "delete":
            self.current_shape = None
            items = self.canvas.find_closest(event.x, event.y)
            if items:
                item_id = items[0]
                self.canvas.delete(item_id)
                self.tables.pop(item_id, None)  # remove from dict if it exists

        elif self.draw_mode == "select":
            self.current_shape = None


        else:
            self.start_x, self.start_y = event.x, event.y
            if self.draw_mode == "rectangle":
                self.current_shape = self.canvas.create_rectangle(
                    self.start_x, self.start_y, self.start_x, self.start_y,
                    outline="black", fill=self.current_color
                )
            elif self.draw_mode == "oval":
                self.current_shape = self.canvas.create_oval(
                    self.start_x, self.start_y, self.start_x, self.start_y,
                    outline="black", fill=self.current_color
               )

    def on_drag(self, event):
        if self.draw_mode == "move" and self.selected_item:
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            self.canvas.move(self.selected_item, dx, dy)
            self.last_x, self.last_y = event.x, event.y

        elif self.draw_mode in ("rectangle", "oval") and self.current_shape:
            self.canvas.coords(self.current_shape, self.start_x, self.start_y, event.x, event.y)

    def on_release(self,event):
        if self.draw_mode in ("rectangle", "oval") and self.current_shape:
            table_size = seat_table()
            self.tables[self.current_shape] = {
                "table_id": self.current_shape,
                "coords": self.canvas.coords(self.current_shape),
                "item_type": self.draw_mode,
                "color": self.current_color,
                "table_size": table_size
            }
            self.current_shape = None
            print(self.tables)

            seat_table()
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


def seat_table() -> int:
    if app.draw_mode == "seating":

        pop_up(app,simpledialog.askinteger, "Table size", "Enter table size:") or 0
    return 0

select_shape(None)
seat_table()
def pop_up(app,dialog_callable,*args,**kwargs):
        x,y = app.winfo_rootx(), app.winfo_rooty()
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
        self.section = section

        Server.server_dict[server_name] = {
            "name": server_name,
            "rotation": rotation,
            "section_name": section,
            "amount_of_tables": None
        }
        print(Server.server_dict)

if __name__ == "__main__":
    #db.delete_database("sections")
    #db.create_datatable()
    #db.delete_servers("")
    #server.get_rotation()
    app.mainloop()
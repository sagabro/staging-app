import tkinter as tk
import databaselogic as db
selected_items = {}

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Real-Time Drawing")


        self.draw_mode = None
        self.current_color = None
        self.selected_item = None
        self.last_x ,self.start_y, self.start_x,self.last_y = 0,0,0,0
        self.current_shape = None

        # Create a specific frame for the list section
        self.list_section_frame = tk.Frame(self)
        self.list_section_frame.pack(side=tk.LEFT, fill="y", padx=5, pady=5)

        entry = tk.Entry(self.list_section_frame) # Parent is now the frame
        entry.pack(fill="x")

        list_box = tk.Listbox(self.list_section_frame) # Parent is now the frame
        list_box.pack(fill="y", expand=True)

        def add_to_list():
            if entry.get():
                list_box.insert(tk.END, entry.get())
                name = entry.get()
                db.insert_server_data(name)
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
        for mode in ["Rectangle", "Oval", "Move", "Paint", "Delete","select"]:
            tk.Button(mode_frame, text=mode,command=lambda m=mode.lower(): self.set_mode(m),bg='black').pack(side=tk.LEFT)

        # Shorter way to create color buttons
        color_frame = tk.Frame(self.btn_frame)
        color_frame.pack(pady=5)
        colors = [("Red", "red"), ("yellow","yellow"), ("Green", "green",), ("orange", "orange")]

        for text, color in colors:
            tk.Button(color_frame, text=text, fg=color, command=lambda c=color: self.set_color(c)).pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self, bg="white", width=400, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)

    def set_color(self, color):
        self.current_color = color

    def select_mode(self):
        if  self.draw_mode == "select":
            item = self.canvas.find_withtag("current")
            self.canvas.itemconfig(item[0], outline="blue")

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

        elif self.draw_mode == "delete":
            self.current_shape = None
            items = self.canvas.find_closest(event.x, event.y)
            if items:
                self.canvas.delete(items[0])

        elif self.draw_mode == "select":
            self.current_shape = None
            items = self.canvas.find_closest(event.x, event.y)
            if items:
                item_id = items[0]
                coords = self.canvas.coords(item_id)
                item_type = self.canvas.type(item_id)

                print(f"Selected item_id={item_id} type={item_type} coords={coords}")

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
class Shapes():
    def __init__(self, table_ids, table_coordinates ,section_name):
        self.table_id = None
        self.table_coordinates = None
        self.section_name = None



class sections():
    def __init__(self, server_name, section_name, rotation):
        self.server_name = None
        self.section_name = None
        self.rotation = None
app = Application()
if __name__ == "__main__":
    #db.delete_database("servers")
    app.mainloop()
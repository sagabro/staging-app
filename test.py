def save_floorchart():
    if app.mode == "save":

def seat_table(self, amount_of_tables):
    if app.mode == "seating":
        amount_of_tables = pop_up(app, simpledialog.askinteger, "Table size", "Enter table size:") or 0


def on_release(self, event):
    tables = {}
    if self.draw_mode in ("rectangle", "oval") and self.current_shape:
        coords = self.canvas.coords(self.current_shape)
        tables[self.current_shape] = {
                "type": self.draw_mode,
                "coords": coords,
                "color": self.current_color,
            }.update(tables)
        print(tables)  # remove this once confirmed working
        self.current_shape = None
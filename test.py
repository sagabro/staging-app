def save_floorchart():
    if app.mode == "save":

def seat_table(self, amount_of_tables):
    if app.mode == "seating":
        amount_of_tables = pop_up(app, simpledialog.askinteger, "Table size", "Enter table size:") or 0

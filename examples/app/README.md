# 🍽️ Restaurant Management System

Hey Ranger! This is your first Python project - a simple restaurant management system.

## 📁 What's in this project?

```
app/
├── main.py              # Main program - start here!
├── models/              # Data structures (Employee, Table)
├── repositories/        # Save/load data to files
├── storage/             # JSON files are saved here
└── requirements.txt     # Python packages needed
```

## 🚀 How to run this

1. **Install packages**: Open terminal and run:
   ```
   pip install -r app/requirements.txt
   ```

2. **Run the program**: 
   ```
   python app/main.py
   ```

## 💡 What does it do?

- Creates 20 employees (waiters, managers, admins)
- Creates 20 tables (numbered 1-20)  
- Saves everything as JSON files in the `storage/` folder
- Only creates new data if files don't exist yet

## 🔍 Key concepts you'll learn

- **Classes**: Employee and Table are data structures
- **JSON**: How to save/load data to files
- **Functions**: Small pieces of code that do one job
- **Lists**: Collections of items (like employees or tables)

## 📝 Try this next

1. Look at the JSON files created in `storage/`
2. Add more employees by editing `main.py`
3. Create a function to find employees by name
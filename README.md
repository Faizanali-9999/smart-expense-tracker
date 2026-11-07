# Smart Expense Tracker

A beginner-friendly personal expense tracking dashboard built with Python, Streamlit, SQLite, Pandas, and Plotly.

## Features

- Add expenses with a date, category, description, and amount.
- View current-month spending and remaining budget.
- See spending by category with an interactive chart.
- View daily spending in a bar chart.
- Browse, edit, and delete transactions.
- Export expense history to CSV.
- Store records in a local SQLite database.

## Requirements

- Python 3.10 or newer
- pip
- VS Code or another Python editor

## Run locally

1. Download or clone this repository.
2. Open the project folder in a terminal.
3. (Recommended) Create and activate a virtual environment:

   **Windows**
   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the application:

   ```bash
   streamlit run app.py
   ```

6. Streamlit will open the app in your browser. If it does not, use the local address printed in the terminal.

## Project structure

```text
smart-expense-tracker/
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
├── assets/
└── utils/
```

## Data storage

The app creates `expenses.db` in the project folder the first time it runs. This database is intentionally excluded from Git using `.gitignore`, so your personal expense records are not uploaded to the repository.

## Important deployment note

This starter version uses a local SQLite file. On many cloud hosting platforms, local files may not persist across restarts or redeployments. For a production deployment, connect a persistent hosted database before relying on it for real records.

## Learning checklist

Use this project to practise:

- Python variables, functions, and imports
- Lists, dictionaries, and loops
- Input validation and exception handling
- SQL tables and CRUD operations
- Data analysis with Pandas
- Interactive charts with Plotly
- Building a web UI with Streamlit
- Git commits and GitHub repository management

## Future improvements

- Add user accounts and authentication.
- Add recurring expenses.
- Add monthly budget limits by category.
- Add filters for date ranges and categories.
- Add automated tests.
- Use a persistent hosted database for deployment.

## License

This project is provided under the MIT License. See `LICENSE`.

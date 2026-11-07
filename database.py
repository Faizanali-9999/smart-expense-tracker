import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "expenses.db"


def get_connection():
    """Open a connection to the local SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create the expenses table if it does not already exist."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                amount REAL NOT NULL CHECK(amount > 0)
            )
            """
        )


def add_expense(expense_date, category, description, amount):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO expenses (date, category, description, amount)
            VALUES (?, ?, ?, ?)
            """,
            (expense_date, category, description, amount),
        )


def get_expenses():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, date, category, description, amount
            FROM expenses
            ORDER BY date DESC, id DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]


def update_expense(expense_id, expense_date, category, description, amount):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE expenses
            SET date = ?, category = ?, description = ?, amount = ?
            WHERE id = ?
            """,
            (expense_date, category, description, amount, expense_id),
        )


def delete_expense(expense_id):
    with get_connection() as connection:
        connection.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))


def get_monthly_total(year, month):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM expenses
            WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
            """,
            (str(year), f"{month:02d}"),
        ).fetchone()
        return float(row["total"])

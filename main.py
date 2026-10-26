import os 
import psycopg
from dotenv import load_dotenv
from fastmcp import FastMCP
import json
from pathlib import Path

load_dotenv()

mcp = FastMCP("ExpenseTracker")
# FastMCP("ExpenseTracker") creates our MCP server object.

CATEGORIES_FILE = Path("resources/categories.json")


@mcp.resource("categories://expense-categories")
def expense_categories():
    """Return the allowed expense categories and subcategories."""

    with open(CATEGORIES_FILE, "r") as file:
        return json.load(file)

    
def get_connection():
    return psycopg.connect(
        dbname="expense_tracker",
        user="postgres",
        password=os.getenv("PG_PASSWORD"),
        host="localhost",
        port=5432
    )
# Whenever our MCP tool needs PostgreSQL, call get_connection() to get a database connection.

@mcp.tool()
# “The function immediately below this decorator should be exposed as an MCP tool.”  
def add_expense(
    date: str, amount: float, category: str, subcategory: str = "", note: str = ""):
    """Add a new expense to the database."""

    with get_connection() as conn:
      # Open a PostgreSQL connection, use it inside this block, and automatically close it when we're finished.
        with conn.cursor() as cur:
        # This creates a cursor, which is the object we'll use to send SQL commands to PostgreSQL.
        # cursor is the object Psycopg gives us to send SQL commands to PostgreSQL and read the results.
        # Think of it as a messenger between Python and the database
            # This opens the cur.execute() call. We'll put the SQL query inside it next.÷
            cur.execute(
                                """
                INSERT INTO expenses
                (date, amount, category, subcategory, note)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (date, amount, category, subcategory, note)
                # Why %s? Psycopg safely substitutes the values for us. We don't build SQL by concatenating user input, which helps prevent SQL injection.
            )
            #  So we're telling PostgreSQL: Insert these five values into the corresponding columns of our expenses table.÷
        
            expense_id = cur.fetchone()[0]
            # Now we need to capture the ID PostgreSQL returns.
    return {
        "status": "success",
        "id": expense_id
    }

# if __name__ == "__main__":
#     result = add_expense(
#         "2026-10-24",
#         250,
#         "Food",
#         "Lunch",
#         "Lunch at office"
#     )

#     print(result)
    # This starts the MCP server, which listens for incoming requests from the FastMCP client.


@mcp.tool()
def list_expenses(start_date: str , end_date: str):
    """List expenses within a date range.""" 

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, date, amount, category, subcategory, note
                FROM expenses
                WHERE date BETWEEN %s AND %s
                ORDER BY id ASC
                """,
                (start_date, end_date)
            )
            
            rows = cur.fetchall()
            return [
                {
                    "id": row[0],
                    "date": str(row[1]),
                    "amount": str(row[2]),
                    "category": row[3],
                    "subcategory": row[4],
                    "note": row[5]
                }
                for row in rows
            ]


# if __name__ == "__main__":
#     result = list_expenses(
#         "2026-10-01",
#         "2026-10-31"
#     )

#     print(result)

        
@mcp.tool()
def summarize(start_date: str, end_date: str, category: str | None = None):
    """Summarize expenses by category."""

    with get_connection() as conn:

        with conn.cursor() as cur:
            if category:
                cur.execute(
                    """
                    SELECT category, SUM(amount) as total
                    FROM expenses
                    WHERE date BETWEEN %s AND %s 
                        AND LOWER(category) = LOWER(%s)
                    GROUP BY category
                    """,
                    (start_date, end_date, category)
                )
            else:
                cur.execute(
                    """
                    SELECT category, SUM(amount) as total
                    FROM expenses
                    WHERE date BETWEEN %s AND %s
                    GROUP BY category
                    """,
                    (start_date, end_date)
                )
            rows = cur.fetchall()
            return [
                {
                    "category": row[0],
                    "total": str(row[1])
                }
                for row in rows
            ]

# if __name__ == "__main__":
#     result = summarize(
#         "2026-10-01",
#         "2026-10-31"
#     )

#     print(result)    

@mcp.tool()
def update_expense(
    expense_id: int,
    date: str | None = None,
    amount: float | None = None,
    category: str | None = None,
    subcategory: str | None = None,
    note: str | None = None
):
    """Update one or more fields of an existing expense."""

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                UPDATE expenses
                SET date = COALESCE(%s, date),
                    amount = COALESCE(%s, amount),
                    category = COALESCE(%s, category),
                    subcategory = COALESCE(%s, subcategory),
                    note = COALESCE(%s, note)
                WHERE id = %s
                RETURNING id
                """,
                (
                    date,
                    amount,
                    category,
                    subcategory,
                    note,
                    expense_id
                )
            )

            updated = cur.fetchone()

            if updated is None:
                return {
                    "status": "error",
                    "message": "Expense not found"
                }

            return {
                "status": "success",
                "id": updated[0]
            }
# if __name__ == "__main__":
#     result = update_expense(
#         1,
#         "2026-10-24",
#         300,
#         "Food",
#         "Dinner",
#         "Dinner at office"
#     )
#     print(result)

@mcp.tool()
def delete_expense(expense_id: int):
    """Delete an existing expense."""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM expenses
                WHERE id = %s
                RETURNING id
                """,
                (expense_id,)
            )

            deleted = cur.fetchone()

            if deleted is None:
                return {
                    "status": "error",
                    "message": "Expense not found"
                }

            return {
                "status": "success",
                "id": deleted[0]
            }
# if __name__ == "__main__":
#     result = delete_expense(1)
#     print(result)

if __name__ == "__main__":
    mcp.run()      
   





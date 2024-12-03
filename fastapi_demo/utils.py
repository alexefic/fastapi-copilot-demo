from datetime import datetime

def log_action(user_id: int, action: str, book_id: int):
    # Implement logging logic here
    print(f"{datetime.now()}: User {user_id} performed {action} on book {book_id}")

class User:
    def __init__(self, id: int, is_solution_sales_manager: bool):
        self.id = id
        self.is_solution_sales_manager = is_solution_sales_manager

# Mock function to get current user
async def get_current_user():
    return User(id=1, is_solution_sales_manager=True)

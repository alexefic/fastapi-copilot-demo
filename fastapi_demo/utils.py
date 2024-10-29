import re
from datetime import datetime

# Utility function to validate ISBN

def validate_isbn(isbn: str) -> bool:
    # Simple regex for ISBN-10 or ISBN-13 validation
    return bool(re.match(r'^(?:ISBN(?:-13)?:? )?(?=[0-9]{13}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)97[89][- ]?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9]$', isbn))

# Utility function to log deletion activity

def log_deletion_activity(user_id: int, isbn: str, books_deleted: list):
    timestamp = datetime.utcnow().isoformat()
    book_titles = [book.title for book in books_deleted]
    log_message = f"User {user_id} deleted books by ISBN {isbn} at {timestamp}. Books deleted: {', '.join(book_titles)}"
    # Here you would typically log to a file or logging service
    print(log_message)
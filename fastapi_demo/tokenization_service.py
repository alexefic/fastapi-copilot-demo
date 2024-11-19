from some_tokenization_library import tokenize

def calculate_tokens(book_content: str) -> int:
    tokens = tokenize(book_content)
    return len(tokens)

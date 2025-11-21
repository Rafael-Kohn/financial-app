def format_currency(value):
    return f"R${value:.2f}"

def simple_text_clean(text):
    return text.strip() if text else ""

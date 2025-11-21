from datetime import datetime

def format_date(date_input):

    if isinstance(date_input, datetime):
        return date_input.strftime("%d/%m/%Y")
    
    if isinstance(date_input, str):
        try:
            # tenta interpretar yyyy-mm-dd
            dt = datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            try:
                # tenta interpretar dd/mm/yyyy
                dt = datetime.strptime(date_input, "%d/%m/%Y")
            except ValueError:
                return date_input  # retorna como está se não conseguir parsear
        return dt.strftime("%d/%m/%Y")
    
    return str(date_input)


def format_currency(value):
    return f"R${value:.2f}"

def simple_text_clean(text):
    return text.strip() if text else ""

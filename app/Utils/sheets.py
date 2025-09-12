from flask import current_app

def get_sheets():
    setup = current_app.config["setup_drive"]
    folder_id = setup.get_or_create_folder()
    sheet_cards = setup.get_or_create_spreadsheet(folder_id, "Cards").sheet1
    sheet_control = setup.get_or_create_spreadsheet(folder_id, "Control").sheet1
    sheet_parcelados = setup.get_or_create_spreadsheet(folder_id, "Parcelados").sheet1
    return sheet_cards, sheet_control, sheet_parcelados

from flask import current_app
from typing import Tuple
from ..Models import Card, Control, Installment, Recurrent

def get_sheets() -> Tuple:
    """
    Retorna os objetos sheet1 das planilhas: Cards, Control e Parcelados.
    Garante que cada planilha exista via setup_drive.
    """
    setup = current_app.config["setup_drive"]
    folder_id = setup.get_or_create_folder()

    # Cria ou abre as planilhas
    sheet_cards = setup.get_or_create_spreadsheet(folder_id, "Cards").sheet1
    sheet_control = setup.get_or_create_spreadsheet(folder_id, "Control").sheet1
    sheet_parcelados = setup.get_or_create_spreadsheet(folder_id, "Installments").sheet1
    sheet_recurrentes = setup.get_or_create_spreadsheet(folder_id, "Recurrent").sheet1

    return sheet_cards, sheet_control, sheet_parcelados, sheet_recurrentes

# ---------- Funções auxiliares ----------

def fetch_controls() -> list[Control]:
    """Busca todas as linhas válidas da planilha Control e converte para objetos Control"""
    _, sheet_control, _, _ = get_sheets()
    rows = sheet_control.get_all_records()
    
    print("DEBUG rows from sheet:", rows)
    return [Control.from_sheet_row(row) for row in rows if row.get("ID")]


def fetch_cards() -> list[Card]:
    """Busca todas as linhas da planilha Cards e converte para objetos Card"""
    sheet_cards, _, _, _ = get_sheets()
    rows = sheet_cards.get_all_records()
    return [Card.from_sheet_row(row) for row in rows]

def fetch_installments() -> list[Installment]:
    """Busca todas as linhas da planilha Parcelados e converte para objetos Installment"""
    _, _, sheet_parcelados, _ = get_sheets()
    rows = sheet_parcelados.get_all_records()
    return [Installment.from_sheet_row(row) for row in rows]

def fetch_recurrentes() -> list[Recurrent]:
    """Busca todas as linhas da planilha Recurrentes e converte para objetos Recurrent"""
    _, _, _, sheet_recurrentes = get_sheets()
    rows = sheet_recurrentes.get_all_records()
    return [Recurrent.from_sheet_row(row) for row in rows]

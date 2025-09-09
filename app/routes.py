from flask import Blueprint, jsonify, request, current_app

bp = Blueprint("routes", __name__)

def get_sheets():
    setup = current_app.config["setup_drive"]
    folder_id = setup.get_or_create_folder()
    sheet_cards = setup.get_or_create_spreadsheet(folder_id, "Cards").sheet1
    sheet_control = setup.get_or_create_spreadsheet(folder_id, "Control").sheet1
    sheet_parcelados = setup.get_or_create_spreadsheet(folder_id, "Parcelados").sheet1
    return sheet_cards, sheet_control, sheet_parcelados

@bp.route("/")
def home():
    return jsonify({"message": "API Finance App funcionando"})

@bp.route("/cards", methods=["POST"])
def add_cards():
    sheet_cards, _, _ = get_sheets()
    data = request.json
    new_row = [
        data.get("id"),
        data.get("nome"),
        data.get("proprietario"),
        data.get("digitos")
    ]
    sheet_cards.append_row(new_row)
    return jsonify({"status": "success", "message": "Cartão adicionado"}), 201

@bp.route("/cartoes", methods=["GET"])
def list_cartoes():
    sheet_cards, _, _ = get_sheets()
    rows = sheet_cards.get_all_records()
    return jsonify(rows)

@bp.route("/control", methods=["POST"])
def add_gasto():
    _, sheet_control, sheet_parcelados = get_sheets()
    data = request.json
    new_row = [
        data.get("id"),
        data.get("nome"),
        data.get("tipo"),
        data.get("valor"),
        data.get("forma"),
        data.get("parcelas"),
        data.get("data"),
        data.get("cartao_id"),
        data.get("modo"),
        "ativo"
    ]
    sheet_control.append_row(new_row)
    if data.get("parcelas", 1) > 1:
        sheet_parcelados.append_row(new_row)
    return jsonify({"status": "success", "message": "Gasto adicionado"}), 201

@bp.route("/control", methods=["GET"])
def list_control():
    _, sheet_control, _ = get_sheets()
    rows = sheet_control.get_all_records()
    return jsonify(rows)

@bp.route("/recorrentes", methods=["POST"])
def add_recorrente():
    _, _, sheet_parcelados = get_sheets()
    data = request.json
    new_row = [
        data.get("id"),
        data.get("nome"),
        data.get("tipo"),
        data.get("valor"),
        data.get("forma"),
        data.get("dia"),
        data.get("cartao_id"),
        data.get("modo"),
        "ativo"
    ]
    sheet_parcelados.append_row(new_row)
    return jsonify({"status": "success", "message": "Gasto recorrente adicionado"}), 201

@bp.route("/recorrentes", methods=["GET"])
def list_recorrentes():
    _, _, sheet_parcelados = get_sheets()
    rows = sheet_parcelados.get_all_records()
    return jsonify(rows)
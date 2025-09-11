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

# --- CRUD para Cards ---
@bp.route("/cards", methods=["POST"])
def add_cards():
    sheet_cards, _, _ = get_sheets()
    data = request.json
    new_row = [
        data.get("ID"),
        data.get("Nome"),
        data.get("Proprietario"),
        data.get("Ultimos_Digitos")
    ]
    sheet_cards.append_row(new_row)
    return jsonify({"status": "success", "message": "Cartão adicionado"}), 201

@bp.route("/cards", methods=["GET"])
def list_cartoes():
    sheet_cards, _, _ = get_sheets()
    rows = sheet_cards.get_all_records()
    return jsonify(rows)

@bp.route("/cards/<int:card_id>", methods=["GET"])
def get_card(card_id):
    sheet_cards, _, _ = get_sheets()
    rows = sheet_cards.get_all_records()
    card = next((row for row in rows if row["ID"] == card_id), None)
    if card:
        return jsonify(card)
    return jsonify({"error": "Cartão não encontrado"}), 404

@bp.route("/cards/<int:card_id>", methods=["PUT", "PATCH"])
def update_card(card_id):
    sheet_cards, _, _ = get_sheets()
    data = request.json
    rows = sheet_cards.get_all_records()
    for idx, row in enumerate(rows, start=2):
        if row["ID"] == card_id:
            sheet_cards.update(f"A{idx}:D{idx}", [[
                data.get("ID", row["ID"]),
                data.get("Nome", row["Nome"]),
                data.get("Proprietario", row["Proprietario"]),
                data.get("Ultimos_Digitos", row["Ultimos_Digitos"])
            ]])
            return jsonify({"status": "success", "message": "Cartão atualizado"})
    return jsonify({"error": "Cartão não encontrado"}), 404

@bp.route("/cards/<int:card_id>", methods=["DELETE"])
def delete_card(card_id):
    sheet_cards, _, _ = get_sheets()
    rows = sheet_cards.get_all_records()
    for idx, row in enumerate(rows, start=2):
        if row["ID"] == card_id:
            sheet_cards.delete_row(idx)
            return jsonify({"status": "success", "message": "Cartão removido"})
    return jsonify({"error": "Cartão não encontrado"}), 404

# --- CRUD para Control ---
@bp.route("/control", methods=["POST"])
def add_gasto():
    _, sheet_control, sheet_parcelados = get_sheets()
    data = request.json
    new_row = [
        data.get("ID"),
        data.get("Nome"),
        data.get("Tipo"),
        data.get("Valor"),
        data.get("Forma"),
        data.get("Parcelas", 1),
        data.get("Data"),
        data.get("Cartao_ID"),
        data.get("Modo"),
        "ativo"
    ]
    sheet_control.append_row(new_row)

    # Se for parcelado, adiciona também em Parcelados
    if int(data.get("Parcelas", 1)) > 1:
        sheet_parcelados.append_row(new_row)

    return jsonify({"status": "success", "message": "Gasto adicionado"}), 201

@bp.route("/control", methods=["GET"])
def list_control():
    _, sheet_control, _ = get_sheets()
    rows = sheet_control.get_all_records()
    return jsonify(rows)

@bp.route("/control/<int:gasto_id>", methods=["GET"])
def get_gasto(gasto_id):
    _, sheet_control, _ = get_sheets()
    rows = sheet_control.get_all_records()
    gasto = next((row for row in rows if row["ID"] == gasto_id), None)
    if gasto:
        return jsonify(gasto)
    return jsonify({"error": "Gasto não encontrado"}), 404

@bp.route("/control/<int:gasto_id>", methods=["PUT", "PATCH"])
def update_gasto(gasto_id):
    _, sheet_control, _ = get_sheets()
    data = request.json
    rows = sheet_control.get_all_records()
    for idx, row in enumerate(rows, start=2):
        if row["ID"] == gasto_id:
            sheet_control.update(f"A{idx}:J{idx}", [[
                data.get("ID", row["ID"]),
                data.get("Nome", row["Nome"]),
                data.get("Tipo", row["Tipo"]),
                data.get("Valor", row["Valor"]),
                data.get("Forma", row["Forma"]),
                data.get("Parcelas", row["Parcelas"]),
                data.get("Data", row["Data"]),
                data.get("Cartao_ID", row["Cartao_ID"]),
                data.get("Modo", row["Modo"]),
                data.get("Status", row["Status"])
            ]])
            return jsonify({"status": "success", "message": "Gasto atualizado"})
    return jsonify({"error": "Gasto não encontrado"}), 404

@bp.route("/control/<int:gasto_id>", methods=["DELETE"])
def delete_gasto(gasto_id):
    _, sheet_control, _ = get_sheets()
    rows = sheet_control.get_all_records()
    for idx, row in enumerate(rows, start=2):
        if row["ID"] == gasto_id:
            sheet_control.delete_rows(idx)
            return jsonify({"status": "success", "message": "Gasto removido"})
    return jsonify({"error": "Gasto não encontrado"}), 404

# --- CRUD para Recorrentes/Parcelados ---
@bp.route("/recorrentes", methods=["POST"])
def add_recorrente():
    _, _, sheet_parcelados = get_sheets()
    data = request.json
    new_row = [
        data.get("ID"),
        data.get("Nome"),
        data.get("Tipo"),
        data.get("Valor"),
        data.get("Forma"),
        data.get("Parcelas", ""),
        data.get("Data", ""),
        data.get("Cartao_ID"),
        data.get("Modo"),
        "ativo"
    ]
    sheet_parcelados.append_row(new_row)
    return jsonify({"status": "success", "message": "Gasto recorrente adicionado"}), 201

@bp.route("/recorrentes", methods=["GET"])
def list_recorrentes():
    _, _, sheet_parcelados = get_sheets()
    rows = sheet_parcelados.get_all_records()
    return jsonify(rows)

@bp.route("/recorrentes/<int:rec_id>", methods=["GET"])
def get_recorrente(rec_id):
    _, _, sheet_parcelados = get_sheets()
    rows = sheet_parcelados.get_all_records()
    rec = next((row for row in rows if row["ID"] == rec_id), None)
    if rec:
        return jsonify(rec)
    return jsonify({"error": "Recorrente não encontrado"}), 404

@bp.route("/recorrentes/<int:rec_id>", methods=["PUT", "PATCH"])
def update_recorrente(rec_id):
    _, _, sheet_parcelados = get_sheets()
    data = request.json
    rows = sheet_parcelados.get_all_records()
    for idx, row in enumerate(rows, start=2):
        if row["ID"] == rec_id:
            sheet_parcelados.update(f"A{idx}:J{idx}", [[
                data.get("ID", row["ID"]),
                data.get("Nome", row["Nome"]),
                data.get("Tipo", row["Tipo"]),
                data.get("Valor", row["Valor"]),
                data.get("Forma", row["Forma"]),
                data.get("Parcelas", row["Parcelas"]),
                data.get("Data", row["Data"]),
                data.get("Cartao_ID", row["Cartao_ID"]),
                data.get("Modo", row["Modo"]),
                data.get("Status", row["Status"])
            ]])
            return jsonify({"status": "success", "message": "Recorrente atualizado"})
    return jsonify({"error": "Recorrente não encontrado"}), 404

@bp.route("/recorrentes/<int:rec_id>", methods=["DELETE"])
def delete_recorrente(rec_id):
    _, _, sheet_parcelados = get_sheets()
    rows = sheet_parcelados.get_all_records()
    for idx, row in enumerate(rows, start=2):
        if row["ID"] == rec_id:
            sheet_parcelados.delete_row(idx)
            return jsonify({"status": "success", "message": "Recorrente removido"})
    return jsonify({"error": "Recorrente não encontrado"}), 404

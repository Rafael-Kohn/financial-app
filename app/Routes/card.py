from flask import Blueprint, jsonify, request
from ..Utils.sheets import get_sheets
from ..Schemas.card import CardSchema

card_bp = Blueprint("cards", __name__)
card_schema = CardSchema()

@card_bp.route("/cards", methods=["POST"])
def add_card():
    data = request.json
    errors = card_schema.validate(data)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    sheet_cards, _, _, _ = get_sheets()
    new_row = [data["ID"], data["Nome"], data["Proprietario"], data["Ultimos_Digitos"]]
    sheet_cards.append_row(new_row)
    return jsonify({"status": "success", "message": "Cartão adicionado"}), 201

@card_bp.route("/cards", methods=["GET"])
def list_cards():
    sheet_cards, _, _, _ = get_sheets()
    rows = sheet_cards.get_all_records()
    return jsonify([card_schema.dump(row) for row in rows])

@card_bp.route("/cards/<int:card_id>", methods=["GET"])
def get_card(card_id):
    sheet_cards, _, _, _ = get_sheets()
    rows = sheet_cards.get_all_records()
    card = next((row for row in rows if row["ID"] == card_id), None)
    if card:
        return jsonify(card_schema.dump(card))
    return jsonify({"error": "Cartão não encontrado"}), 404

@card_bp.route("/cards/<int:card_id>", methods=["PUT", "PATCH"])
def update_card(card_id):
    data = request.json
    errors = card_schema.validate(data, partial=True)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    sheet_cards, _, _, _ = get_sheets()
    rows = sheet_cards.get_all_records()
    for idx, row in enumerate(rows, start=2):
        if row["ID"] == card_id:
            updated_row = [
                data.get("ID", row["ID"]),
                data.get("Nome", row["Nome"]),
                data.get("Proprietario", row["Proprietario"]),
                data.get("Ultimos_Digitos", row["Ultimos_Digitos"])
            ]
            sheet_cards.update(f"A{idx}:D{idx}", [updated_row])
            return jsonify({"status": "success", "message": "Cartão atualizado"})
    return jsonify({"error": "Cartão não encontrado"}), 404

@card_bp.route("/cards/<int:card_id>", methods=["DELETE"])
def delete_card(card_id):
    sheet_cards, _, _, _ = get_sheets()
    rows = sheet_cards.get_all_records()
    for idx, row in enumerate(rows, start=2):
        if row["ID"] == card_id:
            sheet_cards.delete_row(idx)
            return jsonify({"status": "success", "message": "Cartão removido"})
    return jsonify({"error": "Cartão não encontrado"}), 404

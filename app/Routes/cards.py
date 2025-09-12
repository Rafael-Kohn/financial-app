from flask import Blueprint, jsonify, request
from ..Utils.sheets import get_sheets

cards_bp = Blueprint("cards", __name__)

@cards_bp.route("/cards", methods=["POST"])
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

@cards_bp.route("/cards", methods=["GET"])
def list_cartoes():
    sheet_cards, _, _ = get_sheets()
    rows = sheet_cards.get_all_records()
    return jsonify(rows)

@cards_bp.route("/cards/<int:card_id>", methods=["GET"])
def get_card(card_id):
    sheet_cards, _, _ = get_sheets()
    rows = sheet_cards.get_all_records()
    card = next((row for row in rows if row["ID"] == card_id), None)
    if card:
        return jsonify(card)
    return jsonify({"error": "Cartão não encontrado"}), 404

@cards_bp.route("/cards/<int:card_id>", methods=["PUT", "PATCH"])
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

@cards_bp.route("/cards/<int:card_id>", methods=["DELETE"])
def delete_card(card_id):
    sheet_cards, _, _ = get_sheets()
    rows = sheet_cards.get_all_records()
    for idx, row in enumerate(rows, start=2):
        if row["ID"] == card_id:
            sheet_cards.delete_row(idx)
            return jsonify({"status": "success", "message": "Cartão removido"})
    return jsonify({"error": "Cartão não encontrado"}), 404

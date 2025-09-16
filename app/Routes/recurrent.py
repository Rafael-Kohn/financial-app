from flask import Blueprint, jsonify, request
from Utils.sheets import get_sheets

recurrents_bp = Blueprint("recurrent", __name__)

@recurrents_bp.route("/recurrent", methods=["POST"])
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

@recurrents_bp.route("/recurrent", methods=["GET"])
def list_recurrents():
    _, _, sheet_parcelados = get_sheets()
    rows = sheet_parcelados.get_all_records()
    return jsonify(rows)

@recurrents_bp.route("/recurrent/<int:rec_id>", methods=["GET"])
def get_recorrente(rec_id):
    _, _, sheet_parcelados = get_sheets()
    rows = sheet_parcelados.get_all_records()
    rec = next((row for row in rows if row["ID"] == rec_id), None)
    if rec:
        return jsonify(rec)
    return jsonify({"error": "Recorrente não encontrado"}), 404

@recurrents_bp.route("/recurrent/<int:rec_id>", methods=["PUT", "PATCH"])
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

@recurrents_bp.route("/recurrent/<int:rec_id>", methods=["DELETE"])
def delete_recorrente(rec_id):
    _, _, sheet_parcelados = get_sheets()
    rows = sheet_parcelados.get_all_records()
    for idx, row in enumerate(rows, start=2):
        if row["ID"] == rec_id:
            sheet_parcelados.delete_row(idx)
            return jsonify({"status": "success", "message": "Recorrente removido"})
    return jsonify({"error": "Recorrente não encontrado"}), 404

from flask import Blueprint, jsonify, request
from ..Utils.sheets import get_sheets

installment_bp = Blueprint("installment", __name__)

@installment_bp.route("/installment", methods=["POST"])
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

@installment_bp.route("/installment", methods=["GET"])
def list_installment():
    _, _, sheet_parcelados = get_sheets()
    rows = sheet_parcelados.get_all_records()
    return jsonify(rows)

@installment_bp.route("/installment/<int:rec_id>", methods=["GET"])
def get_recorrente(rec_id):
    _, _, sheet_parcelados = get_sheets()
    rows = sheet_parcelados.get_all_records()
    rec = next((row for row in rows if row["ID"] == rec_id), None)
    if rec:
        return jsonify(rec)
    return jsonify({"error": "Parcelado não encontrado"}), 404

@installment_bp.route("/installment/<int:rec_id>", methods=["PUT", "PATCH"])
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
            return jsonify({"status": "success", "message": "Parcelado atualizado"})
    return jsonify({"error": "Parcelado não encontrado"}), 404

@installment_bp.route("/installment/<int:rec_id>", methods=["DELETE"])
def delete_recorrente(rec_id):
    _, _, sheet_parcelados = get_sheets()
    rows = sheet_parcelados.get_all_records()
    for idx, row in enumerate(rows, start=2):
        if row["ID"] == rec_id:
            sheet_parcelados.delete_row(idx)
            return jsonify({"status": "success", "message": "Parcelado removido"})
    return jsonify({"error": "Parcelado não encontrado"}), 404

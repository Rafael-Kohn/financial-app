from flask import Blueprint, jsonify, request
from ..Utils.sheets import get_sheets

control_bp = Blueprint("control", __name__)

@control_bp.route("/control", methods=["POST"])
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

    if int(data.get("Parcelas", 1)) > 1:
        sheet_parcelados.append_row(new_row)

    return jsonify({"status": "success", "message": "Gasto adicionado"}), 201

@control_bp.route("/control", methods=["GET"])
def list_control():
    _, sheet_control, _ = get_sheets()
    rows = sheet_control.get_all_records()
    return jsonify(rows)

@control_bp.route("/control/<int:gasto_id>", methods=["GET"])
def get_gasto(gasto_id):
    _, sheet_control, _ = get_sheets()
    rows = sheet_control.get_all_records()
    gasto = next((row for row in rows if row["ID"] == gasto_id), None)
    if gasto:
        return jsonify(gasto)
    return jsonify({"error": "Gasto não encontrado"}), 404

@control_bp.route("/control/<int:gasto_id>", methods=["PUT", "PATCH"])
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

@control_bp.route("/control/<int:gasto_id>", methods=["DELETE"])
def delete_gasto(gasto_id):
    _, sheet_control, _ = get_sheets()
    rows = sheet_control.get_all_records()
    for idx, row in enumerate(rows, start=2):
        if row["ID"] == gasto_id:
            sheet_control.delete_row(idx)
            return jsonify({"status": "success", "message": "Gasto removido"})
    return jsonify({"error": "Gasto não encontrado"}), 404

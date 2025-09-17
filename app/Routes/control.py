from flask import Blueprint, jsonify, request
from ..Utils.sheets import get_sheets, fetch_controls
from ..Utils.sheets import Control

control_bp = Blueprint("control", __name__)

@control_bp.route("/control", methods=["POST"])
def add_control():
    data = request.json
    try:
        control = Control.from_sheet_row(data)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Dados inválidos: {e}"}), 400

    _, sheet_control, sheet_installment, _ = get_sheets()
    sheet_control.append_row(control.to_sheet_row())

    if control.parcelas > 1:
        sheet_installment.append_row(control.to_sheet_row())

    return jsonify({"status": "success", "message": "Gasto adicionado"}), 201

@control_bp.route("/control", methods=["GET"])
def list_control():
    controls = fetch_controls()
    return jsonify([c.__dict__ for c in controls])

@control_bp.route("/control/<int:gasto_id>", methods=["GET"])
def get_control(gasto_id: int):
    controls = fetch_controls()
    control = next((c for c in controls if c.id == gasto_id), None)
    if control:
        return jsonify(control.__dict__)
    return jsonify({"error": "Gasto não encontrado"}), 404

@control_bp.route("/control/<int:gasto_id>", methods=["PUT", "PATCH"])
def update_control(gasto_id: int):
    data = request.json
    _, sheet_control, _, _ = get_sheets()
    rows = sheet_control.get_all_records()

    for idx, row in enumerate(rows, start=2):
        row_id = row.get("ID") or row.get("Id") or row.get("id")
        if row_id is not None and int(row_id) == gasto_id:
            updated = Control.from_sheet_row({**row, **data})
            sheet_control.update(f"A{idx}:J{idx}", [updated.to_sheet_row()])
            return jsonify({"status": "success", "message": "Gasto atualizado"})

    return jsonify({"error": "Gasto não encontrado"}), 404

@control_bp.route("/control/<int:gasto_id>", methods=["DELETE"])
def delete_control(gasto_id: int):
    _, sheet_control, _, _ = get_sheets()
    rows = sheet_control.get_all_records()

    for idx, row in enumerate(rows, start=2):
        row_id = row.get("ID") or row.get("Id") or row.get("id")
        if row_id is not None and int(row_id) == gasto_id:
            sheet_control.delete_rows(idx)
            return jsonify({"status": "success", "message": "Gasto removido"})

    return jsonify({"error": "Gasto não encontrado"}), 404

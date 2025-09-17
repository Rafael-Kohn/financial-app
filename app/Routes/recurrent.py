from flask import Blueprint, jsonify, request
from ..Utils.sheets import get_sheets
from ..Schemas.recurrent import RecurrentSchema

recurrent_bp = Blueprint("recurrent", __name__)
recurrent_schema = RecurrentSchema()

@recurrent_bp.route("/recurrent", methods=["POST"])
def add_recurrent():
    data = request.json
    errors = recurrent_schema.validate(data)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    _, _, sheet_recurrent = get_sheets()
    new_row = [
        data["ID"], data["Nome"], data["Tipo"], data["Valor"], data["Forma"],
        data.get("Parcelas", ""), data.get("Data", ""), data.get("Cartao_ID"),
        data.get("Modo"), "ativo"
    ]
    sheet_recurrent.append_row(new_row)
    return jsonify({"status": "success", "message": "Recorrente adicionado"}), 201

@recurrent_bp.route("/recurrent", methods=["GET"])
def list_recurrent():
    _, _, sheet_recurrent = get_sheets()
    rows = sheet_recurrent.get_all_records()
    return jsonify([recurrent_schema.dump(row) for row in rows])

@recurrent_bp.route("/recurrent/<int:rec_id>", methods=["GET"])
def get_recurrent(rec_id):
    _, _, sheet_recurrent = get_sheets()
    rows = sheet_recurrent.get_all_records()
    rec = next((row for row in rows if row["ID"] == rec_id), None)
    if rec:
        return jsonify(recurrent_schema.dump(rec))
    return jsonify({"error": "Recorrente não encontrado"}), 404

@recurrent_bp.route("/recurrent/<int:rec_id>", methods=["PUT", "PATCH"])
def update_recurrent(rec_id):
    data = request.json
    errors = recurrent_schema.validate(data, partial=True)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    _, _, sheet_recurrent = get_sheets()
    rows = sheet_recurrent.get_all_records()
    for idx, row in enumerate(rows, start=2):
        if row["ID"] == rec_id:
            updated_row = [
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
            ]
            sheet_recurrent.update(f"A{idx}:J{idx}", [updated_row])
            return jsonify({"status": "success", "message": "Recorrente atualizado"})
    return jsonify({"error": "Recorrente não encontrado"}), 404

@recurrent_bp.route("/recurrent/<int:rec_id>", methods=["DELETE"])
def delete_recurrent(rec_id):
    _, _, sheet_recurrent = get_sheets()
    rows = sheet_recurrent.get_all_records()
    for idx, row in enumerate(rows, start=2):
        if row["ID"] == rec_id:
            sheet_recurrent.delete_row(idx)
            return jsonify({"status": "success", "message": "Recorrente removido"})
    return jsonify({"error": "Recorrente não encontrado"}), 404

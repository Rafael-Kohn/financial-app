from flask import Blueprint, jsonify, request
from ..Utils.sheets import get_sheets
from ..Schemas.installment import InstallmentSchema

installment_bp = Blueprint("installment", __name__)
installment_schema = InstallmentSchema()

@installment_bp.route("/installment", methods=["POST"])
def add_installment():
    data = request.json
    errors = installment_schema.validate(data)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    _, _, sheet_installment = get_sheets()
    new_row = [
        data["ID"], data["Nome"], data["Tipo"], data["Valor"], data["Forma"],
        data.get("Parcelas", ""), data.get("Data", ""), data.get("Cartao_ID"),
        data.get("Modo"), "ativo"
    ]
    sheet_installment.append_row(new_row)
    return jsonify({"status": "success", "message": "Parcelado adicionado"}), 201

@installment_bp.route("/installment", methods=["GET"])
def list_installments():
    _, _, sheet_installment = get_sheets()
    rows = sheet_installment.get_all_records()
    return jsonify([installment_schema.dump(row) for row in rows])

@installment_bp.route("/installment/<int:rec_id>", methods=["GET"])
def get_installment(rec_id):
    _, _, sheet_installment = get_sheets()
    rows = sheet_installment.get_all_records()
    rec = next((row for row in rows if row["ID"] == rec_id), None)
    if rec:
        return jsonify(installment_schema.dump(rec))
    return jsonify({"error": "Parcelado não encontrado"}), 404

@installment_bp.route("/installment/<int:rec_id>", methods=["PUT", "PATCH"])
def update_installment(rec_id):
    data = request.json
    errors = installment_schema.validate(data, partial=True)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    _, _, sheet_installment = get_sheets()
    rows = sheet_installment.get_all_records()
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
            sheet_installment.update(f"A{idx}:J{idx}", [updated_row])
            return jsonify({"status": "success", "message": "Parcelado atualizado"})
    return jsonify({"error": "Parcelado não encontrado"}), 404

@installment_bp.route("/installment/<int:rec_id>", methods=["DELETE"])
def delete_installment(rec_id):
    _, _, sheet_installment = get_sheets()
    rows = sheet_installment.get_all_records()
    for idx, row in enumerate(rows, start=2):
        if row["ID"] == rec_id:
            sheet_installment.delete_row(idx)
            return jsonify({"status": "success", "message": "Parcelado removido"})
    return jsonify({"error": "Parcelado não encontrado"}), 404

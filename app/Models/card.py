from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Card:
    id: int
    nome: str
    proprietario: str
    ultimos_digitos: str

    @classmethod
    def from_sheet_row(cls, row: Dict[str, Any]):
        # row vindo de gspread.get_all_records() -> chaves são os cabeçalhos da planilha
        return cls(
            id=int(row.get("ID") or row.get("Id") or row.get("id")),
            nome=row.get("Nome") or row.get("nome") or "",
            proprietario=row.get("Proprietario") or row.get("proprietário") or "",
            ultimos_digitos=str(row.get("Ultimos_Digitos") or row.get("Ultimos_Dígitos") or row.get("digitos") or "")
        )

    def to_sheet_row(self):
        # formato que o routes espera ao inserir na planilha
        return [self.id, self.nome, self.proprietario, self.ultimos_digitos]

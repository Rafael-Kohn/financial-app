from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Recurrent:
    id: int
    nome: str
    tipo: str
    valor: float
    forma: str
    parcelas: Optional[int] = None
    data: Optional[str] = None
    cartao_id: Optional[int] = None
    modo: Optional[str] = None
    status: str = "ativo"

    @classmethod
    def from_sheet_row(cls, row: Dict[str, Any]):
        parcelas_val = row.get("Parcelas")
        return cls(
            id=int(row.get("ID") or row.get("Id") or row.get("id")),
            nome=row.get("Nome") or "",
            tipo=row.get("Tipo") or "",
            valor=float(row.get("Valor") or 0.0),
            forma=row.get("Forma") or "",
            parcelas=(int(parcelas_val) if parcelas_val not in (None, "", "None") else None),
            data=row.get("Data") or None,
            cartao_id=(int(row.get("Cartao_ID")) if row.get("Cartao_ID") not in (None, "", "None") else None),
            modo=row.get("Modo") or None,
            status=row.get("Status") or "ativo",
        )

    def to_sheet_row(self):
        return [
            self.id,
            self.nome,
            self.tipo,
            self.valor,
            self.forma,
            self.parcelas if self.parcelas is not None else "",
            self.data or "",
            self.cartao_id if self.cartao_id is not None else "",
            self.modo or "",
            self.status,
        ]

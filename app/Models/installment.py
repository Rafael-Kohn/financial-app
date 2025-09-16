from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Installment:
    id: int
    numero: int
    valor: float
    vencimento: str
    pago: bool = False
    control_id: Optional[int] = None

    @classmethod
    def from_sheet_row(cls, row: Dict[str, Any]):
        return cls(
            id=int(row.get("ID") or row.get("Id") or row.get("id")),
            numero=int(row.get("Numero") or row.get("numero") or 0),
            valor=float(row.get("Valor") or 0.0),
            vencimento=row.get("Vencimento") or "",
            pago=bool(row.get("Pago") in (True, "True", "true", "TRUE", "1", 1)),
            control_id=(int(row.get("Control_ID")) if row.get("Control_ID") not in (None, "", "None") else None),
        )

    def to_sheet_row(self):
        return [
            self.id,
            self.numero,
            self.valor,
            self.vencimento,
            "TRUE" if self.pago else "FALSE",
            self.control_id if self.control_id is not None else ""
        ]

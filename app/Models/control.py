from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class Control:
    id: int
    nome: str
    tipo: str
    valor: float
    forma: str
    parcelas: int = 1
    data: Optional[str] = None
    cartao_id: Optional[int] = None
    modo: Optional[str] = None
    status: str = "ativo"

    @classmethod
    def from_sheet_row(cls, row: Dict[str, Any]):
        # Trata valor com vírgula ou ponto
        valor_raw = row.get("Valor") or row.get("VALOR") or row.get("valor") or 0.0
        if isinstance(valor_raw, str):
            valor = float(valor_raw.replace(",", "."))
        else:
            valor = float(valor_raw)
        # Trata parcelas
        parcelas_raw = row.get("Parcelas") or row.get("PARCELAS") or row.get("parcelas") or 1
        try:
            parcelas = int(parcelas_raw)
        except Exception:
            parcelas = 1
        # Trata cartao_id
        cartao_id_raw = row.get("Cartao_ID") or row.get("CARTAO_ID") or row.get("cartao_id")
        try:
            cartao_id = int(cartao_id_raw) if cartao_id_raw not in (None, "", "None") else None
        except Exception:
            cartao_id = None
        return cls(
            id=int(row.get("ID") or row.get("Id") or row.get("id")),
            nome=row.get("Nome") or row.get("NOME") or row.get("nome") or "",
            tipo=row.get("Tipo") or row.get("TIPO") or row.get("tipo") or "",
            valor=valor,
            forma=row.get("Forma") or row.get("FORMA") or row.get("forma") or "",
            parcelas=parcelas,
            data=row.get("Data") or row.get("DATA") or row.get("data") or None,
            cartao_id=cartao_id,
            modo=row.get("Modo") or row.get("MODO") or row.get("modo") or None,
            status=row.get("Status") or row.get("STATUS") or row.get("status") or "ativo",
        )

    def to_sheet_row(self):
        return [
            self.id,
            self.nome,
            self.tipo,
            self.valor,
            self.forma,
            self.parcelas,
            self.data or "",
            self.cartao_id if
            self.cartao_id is not None else "",
            self.modo or "",]
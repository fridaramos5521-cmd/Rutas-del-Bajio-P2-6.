"""Entidades simples con identificadores para persistencia CSV."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Cliente:
    id: str
    nombre: str
    telefono: str

@dataclass(frozen=True)
class Ruta:
    id: str
    origen: str
    destino: str

@dataclass(frozen=True)
class Pedido:
    id: str
    cliente_id: str
    ruta_id: str
    descripcion: str
    cantidad: int
    estado: str = 'pendiente'

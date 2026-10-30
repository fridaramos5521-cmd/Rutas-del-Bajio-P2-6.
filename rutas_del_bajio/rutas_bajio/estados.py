"""Maquina de estados de pedidos."""
from .errores import TransicionInvalida

TRANSICIONES = {
    'pendiente': frozenset({'en_transito', 'cancelado'}),
    'en_transito': frozenset({'entregado'}),
    'entregado': frozenset(),
    'cancelado': frozenset(),
}

def validar_transicion(actual: str, nuevo: str) -> None:
    """Rechaza un destino no permitido y deja el origen intacto."""
    if nuevo not in TRANSICIONES.get(actual, frozenset()):
        raise TransicionInvalida(f'{actual} -> {nuevo} no esta permitido')

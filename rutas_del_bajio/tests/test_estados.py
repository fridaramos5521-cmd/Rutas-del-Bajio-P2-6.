import pytest
from rutas_bajio import Pedido, SistemaRutas
from rutas_bajio.errores import TransicionInvalida, DatoInvalido

@pytest.fixture
def creado(sistema):
    sistema.crear_pedido(Pedido('P-01', 'C-01', 'R-01', 'Paquete', 1))
    return sistema

def test_pendiente_a_transito(creado):
    assert creado.cambiar_estado('P-01', 'en_transito').estado == 'en_transito'

def test_transito_a_entregado(creado):
    creado.cambiar_estado('P-01', 'en_transito')
    assert creado.cambiar_estado('P-01', 'entregado').estado == 'entregado'

def test_pendiente_a_cancelado(creado):
    assert creado.cambiar_estado('P-01', 'cancelado').estado == 'cancelado'

@pytest.mark.parametrize('origen,destino', [('pendiente','entregado'), ('en_transito','pendiente'), ('entregado','pendiente'), ('cancelado','en_transito')])
def test_transicion_prohibida_sin_escritura(creado, origen, destino):
    if origen == 'en_transito' or origen == 'entregado':
        creado.cambiar_estado('P-01', 'en_transito')
    if origen == 'entregado':
        creado.cambiar_estado('P-01', 'entregado')
    if origen == 'cancelado':
        creado.cambiar_estado('P-01', 'cancelado')
    antes = creado.db.ruta('pedidos').read_bytes()
    with pytest.raises(TransicionInvalida):
        creado.cambiar_estado('P-01', destino)
    assert creado.db.ruta('pedidos').read_bytes() == antes

def test_estado_persiste(creado):
    creado.cambiar_estado('P-01', 'en_transito')
    recargado = SistemaRutas(creado.db.directorio)
    assert recargado.consultar_pedido('P-01').estado == 'en_transito'

def test_no_editar_entregado(creado):
    creado.cambiar_estado('P-01', 'en_transito')
    creado.cambiar_estado('P-01', 'entregado')
    with pytest.raises(DatoInvalido):
        creado.actualizar_pedido('P-01', 'Otro', 4)

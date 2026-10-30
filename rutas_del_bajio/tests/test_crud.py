import pytest
from rutas_bajio import Cliente, Ruta, Pedido, SistemaRutas
from rutas_bajio.errores import DatoInvalido, RegistroDuplicado, RegistroNoEncontrado, ReferenciaInvalida


def pedido(id='P-01', **changes):
    return Pedido(id, changes.get('cliente_id', 'C-01'), changes.get('ruta_id', 'R-01'), changes.get('descripcion', 'Paquete'), changes.get('cantidad', 2), changes.get('estado', 'pendiente'))

def test_cliente_crear_y_consultar(sistema):
    assert sistema.consultar_cliente('C-01').nombre == 'Ana López'

def test_cliente_actualizar(sistema):
    assert sistema.actualizar_cliente('C-01', 'Ana M', '4778888888').nombre == 'Ana M'

def test_cliente_eliminar(sistema):
    sistema.eliminar_cliente('C-01')
    with pytest.raises(RegistroNoEncontrado):
        sistema.consultar_cliente('C-01')

def test_cliente_duplicado(sistema):
    with pytest.raises(RegistroDuplicado):
        sistema.crear_cliente(Cliente('C-01', 'Otra', '999'))

def test_ruta_actualizar(sistema):
    assert sistema.actualizar_ruta('R-01', 'León', 'Irapuato').destino == 'Irapuato'

def test_ruta_eliminar(sistema):
    sistema.eliminar_ruta('R-01')
    assert sistema.listar_rutas() == []

def test_ruta_duplicada(sistema):
    with pytest.raises(RegistroDuplicado):
        sistema.crear_ruta(Ruta('R-01', 'A', 'B'))

def test_crear_y_consultar_pedido(sistema):
    sistema.crear_pedido(pedido())
    assert sistema.consultar_pedido('P-01').cantidad == 2

def test_actualizar_pedido(sistema):
    sistema.crear_pedido(pedido())
    assert sistema.actualizar_pedido('P-01', 'Nuevo', 4).cantidad == 4

def test_eliminar_pedido(sistema):
    sistema.crear_pedido(pedido())
    sistema.eliminar_pedido('P-01')
    assert sistema.listar_pedidos() == []

def test_llave_cliente_inexistente(sistema):
    with pytest.raises(ReferenciaInvalida):
        sistema.crear_pedido(pedido(cliente_id='C-404'))

def test_llave_ruta_inexistente(sistema):
    with pytest.raises(ReferenciaInvalida):
        sistema.crear_pedido(pedido(ruta_id='R-404'))

def test_no_borrar_cliente_referenciado(sistema):
    sistema.crear_pedido(pedido())
    with pytest.raises(ReferenciaInvalida):
        sistema.eliminar_cliente('C-01')

def test_no_borrar_ruta_referenciada(sistema):
    sistema.crear_pedido(pedido())
    with pytest.raises(ReferenciaInvalida):
        sistema.eliminar_ruta('R-01')

def test_cantidad_negativa(sistema):
    with pytest.raises(DatoInvalido):
        sistema.crear_pedido(pedido(cantidad=-3))

def test_pedido_id_duplicado(sistema):
    sistema.crear_pedido(pedido())
    with pytest.raises(RegistroDuplicado):
        sistema.crear_pedido(pedido())

def test_persistencia_recarga(sistema):
    sistema.crear_pedido(pedido())
    nuevo = SistemaRutas(sistema.db.directorio)
    assert nuevo.consultar_pedido('P-01').cantidad == 2

def test_obligatorio_vacio(sistema):
    with pytest.raises(DatoInvalido):
        sistema.crear_cliente(Cliente('C-02', '  ', '999'))

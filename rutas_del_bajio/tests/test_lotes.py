import csv
import pytest
from rutas_bajio.lotes import cargar_pedidos, COLUMNAS
from rutas_bajio.errores import ArchivoLoteInvalido

def hacer_csv(tmp_path, filas, campos=COLUMNAS):
    archivo = tmp_path / 'lote.csv'
    with archivo.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(filas)
    return archivo

def fila(id='P-01', **cambios):
    return {'id': id, 'cliente_id': 'C-01', 'ruta_id': 'R-01', 'descripcion': '  Caja  ', 'cantidad': ' 2 ', 'estado': ' PENDIENTE ', **cambios}

def test_lote_valido_y_limpieza(sistema, tmp_path):
    reporte = cargar_pedidos(sistema, hacer_csv(tmp_path, [fila()]))
    assert reporte.aceptadas == 1 and not reporte.rechazadas
    assert sistema.consultar_pedido('P-01').descripcion == 'Caja'

def test_lote_mixto_y_rechazos(sistema, tmp_path):
    reporte = cargar_pedidos(sistema, hacer_csv(tmp_path, [fila(), fila('P-02', cantidad='-1'), fila('P-03')]), tmp_path/'rechazos.csv')
    assert reporte.aceptadas == 2
    assert len(reporte.rechazadas) == 1 and reporte.rechazadas[0].linea == 3
    assert (tmp_path/'rechazos.csv').read_text(encoding='utf-8').startswith('linea,id,motivo')

def test_duplicado_en_lote(sistema, tmp_path):
    reporte = cargar_pedidos(sistema, hacer_csv(tmp_path, [fila(), fila()]))
    assert reporte.aceptadas == 1 and len(reporte.rechazadas) == 1

def test_encabezado_ausente_detiene_lote(sistema, tmp_path):
    archivo = hacer_csv(tmp_path, [{'id':'P-01'}], ['id'])
    with pytest.raises(ArchivoLoteInvalido):
        cargar_pedidos(sistema, archivo)
    assert sistema.listar_pedidos() == []

def test_lote_fk_invalida(sistema, tmp_path):
    reporte = cargar_pedidos(sistema, hacer_csv(tmp_path, [fila(cliente_id='C-99')]))
    assert reporte.aceptadas == 0 and len(reporte.rechazadas) == 1

def test_lote_estado_vacio_se_normaliza(sistema, tmp_path):
    reporte = cargar_pedidos(sistema, hacer_csv(tmp_path, [fila(estado='  ')]))
    assert reporte.aceptadas == 1
    assert sistema.consultar_pedido('P-01').estado == 'pendiente'

def test_lote_numero_invalido(sistema, tmp_path):
    reporte = cargar_pedidos(sistema, hacer_csv(tmp_path, [fila(cantidad='dos')]))
    assert len(reporte.rechazadas) == 1

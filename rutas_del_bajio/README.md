# Rutas del Bajio - Proyecto Segundo Parcial

Backend de referencia para el caso de clase: Clientes, Rutas, Pedidos, CRUD, persistencia CSV, maquina de estados y carga por lotes.

## Instalacion y pruebas

```bash
python -m pip install -e '.[test]'
python -m pytest -v
```

## Ejecucion en Google Colab

Subir y descomprimir el ZIP; luego abrir una celda en la carpeta del proyecto:

```python
%cd /content/rutas_del_bajio
!python -m pip install -e '.[test]'
!python -m pytest -v
```

## Modelo

- Cliente: id, nombre, telefono.
- Ruta: id, origen, destino.
- Pedido: id, cliente_id, ruta_id, descripcion, cantidad, estado.
- Estados: pendiente -> en_transito -> entregado; pendiente -> cancelado.
- CSV en carpeta seleccionada al instanciar `SistemaRutas`.

## Ejemplo minimo

```python
from rutas_bajio import SistemaRutas, Cliente, Ruta, Pedido
from rutas_bajio.lotes import cargar_pedidos
sistema = SistemaRutas('datos')
sistema.crear_cliente(Cliente('C-01', 'Ana', '4771234567'))
sistema.crear_ruta(Ruta('R-01', 'Leon', 'Celaya'))
sistema.crear_pedido(Pedido('P-01', 'C-01', 'R-01', 'Caja', 2))
sistema.cambiar_estado('P-01', 'en_transito')
```

## Entrega

Para GitHub, inicializar el repositorio, subir el codigo y pruebas, obtener aportes reales de los cuatro integrantes y registrar al final `git commit -m 'v-p2 - entrega final'`. No se ha realizado ninguna operacion remota desde este ZIP.

**Nota academica:** Codigo y reporte de apoyo generados con IA, sujetos a revision, personalizacion, pruebas y declaracion de uso acorde a la guia del curso. La guia indica que los capitulos finales deben ser redactados por los estudiantes.

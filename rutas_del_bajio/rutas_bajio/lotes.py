"""Carga por lotes con rechazos por fila y errores de estructura."""
import csv
from dataclasses import dataclass, field
from pathlib import Path
from .modelos import Pedido
from .errores import ArchivoLoteInvalido, ErrorRutas

COLUMNAS = ['id', 'cliente_id', 'ruta_id', 'descripcion', 'cantidad', 'estado']

@dataclass
class Rechazo:
    linea: int
    id: str
    motivo: str

@dataclass
class ReporteLote:
    aceptadas: int = 0
    rechazadas: list[Rechazo] = field(default_factory=list)

def cargar_pedidos(sistema, archivo_csv, archivo_rechazos=None) -> ReporteLote:
    """Procesa filas independientes; ausencia de encabezados detiene el lote."""
    reporte = ReporteLote()
    with Path(archivo_csv).open('r', newline='', encoding='utf-8-sig') as archivo:
        lector = csv.DictReader(archivo)
        if not lector.fieldnames or any(c not in lector.fieldnames for c in COLUMNAS):
            raise ArchivoLoteInvalido('encabezados obligatorios ausentes')
        for linea, fila in enumerate(lector, start=2):
            identificador = (fila.get('id') or '').strip()
            try:
                if None in fila or any(fila.get(c) is None for c in COLUMNAS):
                    raise ArchivoLoteInvalido('numero de columnas incorrecto')
                datos = {c: str(fila[c]).strip() for c in COLUMNAS}
                datos['estado'] = datos['estado'].lower() or 'pendiente'
                pedido = Pedido(**datos)
                sistema.crear_pedido(pedido)
                reporte.aceptadas += 1
            except ErrorRutas as exc:
                reporte.rechazadas.append(Rechazo(linea, identificador, str(exc)))
    if archivo_rechazos is not None:
        with Path(archivo_rechazos).open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['linea', 'id', 'motivo'])
            writer.writeheader()
            for rechazo in reporte.rechazadas:
                writer.writerow(vars(rechazo))
    return reporte

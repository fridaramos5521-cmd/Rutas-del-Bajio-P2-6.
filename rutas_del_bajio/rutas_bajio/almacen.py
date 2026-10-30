"""Lectura y reemplazo atomico de archivos CSV."""
import csv
import os
import tempfile
from pathlib import Path

ESQUEMAS = {
    'clientes': ['id', 'nombre', 'telefono'],
    'rutas': ['id', 'origen', 'destino'],
    'pedidos': ['id', 'cliente_id', 'ruta_id', 'descripcion', 'cantidad', 'estado'],
}

class AlmacenCSV:
    def __init__(self, directorio):
        self.directorio = Path(directorio)
        self.directorio.mkdir(parents=True, exist_ok=True)
        for tabla, campos in ESQUEMAS.items():
            if not self.ruta(tabla).exists():
                self.escribir(tabla, [])

    def ruta(self, tabla):
        return self.directorio / f'{tabla}.csv'

    def leer(self, tabla):
        with self.ruta(tabla).open('r', newline='', encoding='utf-8-sig') as archivo:
            return list(csv.DictReader(archivo))

    def escribir(self, tabla, registros):
        campos = ESQUEMAS[tabla]
        fd, temporal = tempfile.mkstemp(prefix=f'.{tabla}_', suffix='.csv', dir=self.directorio)
        try:
            with os.fdopen(fd, 'w', newline='', encoding='utf-8') as archivo:
                writer = csv.DictWriter(archivo, fieldnames=campos)
                writer.writeheader()
                writer.writerows(registros)
            os.replace(temporal, self.ruta(tabla))
        finally:
            if os.path.exists(temporal):
                os.unlink(temporal)

import pytest
from rutas_bajio import Cliente, Ruta, SistemaRutas

@pytest.fixture
def sistema(tmp_path):
    s = SistemaRutas(tmp_path)
    s.crear_cliente(Cliente('C-01', 'Ana López', '4771234567'))
    s.crear_ruta(Ruta('R-01', 'León', 'Celaya'))
    return s

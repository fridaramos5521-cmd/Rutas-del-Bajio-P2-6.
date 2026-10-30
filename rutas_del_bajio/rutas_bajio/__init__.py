"""Backend CSV para Rutas del Bajio."""
from .modelos import Cliente, Ruta, Pedido
from .gestores import SistemaRutas
from .errores import DatoInvalido, RegistroDuplicado, RegistroNoEncontrado, ReferenciaInvalida, TransicionInvalida

"""Excepciones del dominio."""
class ErrorRutas(Exception):
    """Error de negocio del sistema."""
class DatoInvalido(ErrorRutas):
    """Un campo no satisface las reglas."""
class RegistroDuplicado(ErrorRutas):
    """El identificador ya existe."""
class RegistroNoEncontrado(ErrorRutas):
    """No existe el identificador solicitado."""
class ReferenciaInvalida(ErrorRutas):
    """La llave foranea no existe o esta en uso."""
class TransicionInvalida(ErrorRutas):
    """El cambio de estado no esta permitido."""
class ArchivoLoteInvalido(ErrorRutas):
    """El archivo CSV no tiene estructura valida."""

"""Servicios CRUD; integridad referencial y estados."""
from dataclasses import asdict, replace
from .almacen import AlmacenCSV
from .modelos import Cliente, Ruta, Pedido
from .estados import TRANSICIONES, validar_transicion
from .errores import DatoInvalido, RegistroDuplicado, RegistroNoEncontrado, ReferenciaInvalida


def obligatorio(valor, campo):
    resultado = str(valor).strip()
    if not resultado:
        raise DatoInvalido(f'{campo} es obligatorio')
    return resultado

class SistemaRutas:
    """Interfaz de operaciones sobre tres entidades persistidas en CSV."""
    def __init__(self, directorio):
        self.db = AlmacenCSV(directorio)

    def _buscar(self, tabla, id):
        for fila in self.db.leer(tabla):
            if fila['id'] == id:
                return fila
        raise RegistroNoEncontrado(f'{tabla}: {id}')

    def _crear(self, tabla, registro):
        filas = self.db.leer(tabla)
        if any(f['id'] == registro['id'] for f in filas):
            raise RegistroDuplicado(registro['id'])
        self.db.escribir(tabla, filas + [registro])

    def _actualizar(self, tabla, id, registro):
        filas = self.db.leer(tabla)
        for i, fila in enumerate(filas):
            if fila['id'] == id:
                filas[i] = registro
                self.db.escribir(tabla, filas)
                return
        raise RegistroNoEncontrado(f'{tabla}: {id}')

    def _eliminar(self, tabla, id):
        filas = self.db.leer(tabla)
        restantes = [f for f in filas if f['id'] != id]
        if len(restantes) == len(filas):
            raise RegistroNoEncontrado(f'{tabla}: {id}')
        self.db.escribir(tabla, restantes)

    def crear_cliente(self, cliente: Cliente) -> Cliente:
        limpio = Cliente(*(obligatorio(v, k) for k, v in asdict(cliente).items()))
        self._crear('clientes', asdict(limpio))
        return limpio

    def consultar_cliente(self, id: str) -> Cliente:
        return Cliente(**self._buscar('clientes', id))

    def actualizar_cliente(self, id: str, nombre: str, telefono: str) -> Cliente:
        self.consultar_cliente(id)
        nuevo = Cliente(id, obligatorio(nombre, 'nombre'), obligatorio(telefono, 'telefono'))
        self._actualizar('clientes', id, asdict(nuevo))
        return nuevo

    def eliminar_cliente(self, id: str) -> None:
        if any(f['cliente_id'] == id for f in self.db.leer('pedidos')):
            raise ReferenciaInvalida('cliente tiene pedidos')
        self._eliminar('clientes', id)

    def listar_clientes(self):
        return [Cliente(**fila) for fila in self.db.leer('clientes')]

    def crear_ruta(self, ruta: Ruta) -> Ruta:
        limpia = Ruta(*(obligatorio(v, k) for k, v in asdict(ruta).items()))
        self._crear('rutas', asdict(limpia))
        return limpia

    def consultar_ruta(self, id: str) -> Ruta:
        return Ruta(**self._buscar('rutas', id))

    def actualizar_ruta(self, id: str, origen: str, destino: str) -> Ruta:
        self.consultar_ruta(id)
        nueva = Ruta(id, obligatorio(origen, 'origen'), obligatorio(destino, 'destino'))
        self._actualizar('rutas', id, asdict(nueva))
        return nueva

    def eliminar_ruta(self, id: str) -> None:
        if any(f['ruta_id'] == id for f in self.db.leer('pedidos')):
            raise ReferenciaInvalida('ruta tiene pedidos')
        self._eliminar('rutas', id)

    def listar_rutas(self):
        return [Ruta(**fila) for fila in self.db.leer('rutas')]

    def _validar_pedido(self, pedido):
        datos = asdict(pedido)
        for campo in ('id', 'cliente_id', 'ruta_id', 'descripcion'):
            datos[campo] = obligatorio(datos[campo], campo)
        try:
            datos['cantidad'] = int(str(datos['cantidad']).strip())
        except ValueError as exc:
            raise DatoInvalido('cantidad no numerica') from exc
        if datos['cantidad'] <= 0:
            raise DatoInvalido('cantidad debe ser positiva')
        if datos['estado'] not in TRANSICIONES:
            raise DatoInvalido('estado desconocido')
        if datos['estado'] != 'pendiente':
            raise DatoInvalido('un pedido nuevo debe iniciar pendiente')
        try:
            self.consultar_cliente(datos['cliente_id'])
            self.consultar_ruta(datos['ruta_id'])
        except RegistroNoEncontrado as exc:
            raise ReferenciaInvalida(str(exc)) from exc
        return Pedido(**datos)

    def crear_pedido(self, pedido: Pedido) -> Pedido:
        limpio = self._validar_pedido(pedido)
        self._crear('pedidos', asdict(limpio))
        return limpio

    def consultar_pedido(self, id: str) -> Pedido:
        fila = self._buscar('pedidos', id)
        return Pedido(**{**fila, 'cantidad': int(fila['cantidad'])})

    def listar_pedidos(self):
        return [Pedido(**{**f, 'cantidad': int(f['cantidad'])}) for f in self.db.leer('pedidos')]

    def actualizar_pedido(self, id: str, descripcion: str, cantidad: int) -> Pedido:
        actual = self.consultar_pedido(id)
        if actual.estado != 'pendiente':
            raise DatoInvalido('solo se edita un pedido pendiente')
        nuevo = self._validar_pedido(replace(actual, descripcion=descripcion, cantidad=cantidad))
        self._actualizar('pedidos', id, asdict(nuevo))
        return nuevo

    def eliminar_pedido(self, id: str) -> None:
        actual = self.consultar_pedido(id)
        if actual.estado != 'pendiente':
            raise DatoInvalido('solo se elimina un pedido pendiente')
        self._eliminar('pedidos', id)

    def cambiar_estado(self, id: str, nuevo_estado: str) -> Pedido:
        actual = self.consultar_pedido(id)
        validar_transicion(actual.estado, nuevo_estado)
        cambiado = replace(actual, estado=nuevo_estado)
        self._actualizar('pedidos', id, asdict(cambiado))
        return cambiado

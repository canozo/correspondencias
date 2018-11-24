# Correspondencia asociativa por conjuntos con sustitución secuencial
# (con 2 conjuntos, cada conjunto 4 líneas)
# pareciera ser lo mismo que lru

LINEAS = 16
CACHE = 8
CONJUNTOS = 2

PRUEBA = {
  20: ['400-430', '812-830'],
  16: ['820-840', '1432-1455']
}

CRYS = {
  13: ['7112-7182', '5128-5159'],
  15: ['5138-5208', '13652-13702']
}

class Linea:
  def __init__(self, disponible, num_linea=0, desde=0, hasta=0, antiguedad=0, size=LINEAS):
    self.size = size
    self.num_linea = num_linea
    self.disponible = disponible
    self.desde = desde
    self.hasta = hasta
    self.antiguedad = antiguedad

  def existe(self, valor):
    return self.desde <= valor <= self.hasta


class Cache:
  def __init__(self, entrada, size=CACHE, size_lineas=LINEAS):
    self.lineas = [Linea(True, num_linea=x, size=size_lineas) for x in range(size)]
    self.entrada = entrada
    self.size_lineas = size_lineas
    self.lecturas = []
    self.direcciones = []

    for num_veces in entrada:
      for x in range(len(entrada[num_veces])):
        self.lecturas.append(num_veces)
        self.direcciones.append(entrada[num_veces].pop(0))
    self.num_direcciones = len(self.lecturas)

  def __str__(self):
    result = ''
    for i, linea in enumerate(self.lineas):
      result += f'{i} | disp: {linea.disponible}\t| ant: {linea.antiguedad} | {linea.desde}\t{linea.hasta}\n'
    return result

  def existe_en_cache(self, valor):
    for linea in self.lineas:
      if linea.existe(valor):
        return True
    return False

  def agregar_linea(self, desde, hasta, pos, conjunto):
    # agregar una linea cuando hay un espacio vacio
    # disminuir la antiguedad de las lineas viejas
    i, j = self.get_rango_conjunto(conjunto)

    for x in range(i, j):
      linea = self.lineas[x]
      if linea.disponible:
        continue
      linea.antiguedad -= 1

    self.lineas[pos] = Linea(False, desde=desde, hasta=hasta, antiguedad=4)

  def agregar_linea_lru(self, desde, hasta, conjunto):
    print(self)
    # agregar una linea cuando todas estan ocupadas, reemplazar la mas vieja
    i, j = self.get_rango_conjunto(conjunto)
    pos_linea = -1

    for pos in range(i, j):
      linea = self.lineas[pos]
      if linea.antiguedad == 1:
        pos_linea = pos
      else:
        linea.antiguedad -= 1

    self.lineas[pos_linea] = Linea(False, desde=desde, hasta=hasta, antiguedad=4)

  def get_rango_conjunto(self, conjunto):
    if conjunto == 0:
      return 0, 4
    else:
      return 4, 8

  def buscar_disponible(self, conjunto):
    i, j = self.get_rango_conjunto(conjunto)

    for pos in range(i, j):
      if self.lineas[pos].disponible:
        return pos

    return -1

  def resolver(self):
    aciertos = 0
    fallos = 0

    while max(self.lecturas) != 0:
      for i in range(self.num_direcciones):

        if self.lecturas[i] == 0:
          continue

        desde, hasta = map(int, self.direcciones[i].split('-'))

        while desde <= hasta:
          bloque = desde // self.size_lineas
          conjunto = bloque % CONJUNTOS
          fin_bloque = self.size_lineas * bloque + self.size_lineas - 1

          disponible = self.buscar_disponible(conjunto)

          if self.existe_en_cache(desde):
            # ya esta en la cache
            aciertos += 1

          elif disponible == -1:
            # buscar la mas vieja y reemplazarla
            self.agregar_linea_lru(bloque * self.size_lineas, fin_bloque, conjunto)

            # falla una vez porque no esta en cache
            fallos += 1

          else:
            # no esta en la cache pero hay una posicion disponible
            # la ingresamos en la posicion disponible
            self.agregar_linea(bloque * self.size_lineas, fin_bloque, disponible, conjunto)

            # falla una vez porque no esta en cache
            fallos += 1

          # nos movemos a la siguiente palabra
          desde += 1

        self.lecturas[i] -= 1

    porcentaje = (aciertos / (aciertos + fallos)) * 100
    print(self)
    print(f'Aciertos: {aciertos}\nFallos: {fallos}\nPorcentaje de aciertos: {porcentaje}%')


def run(prueba=True):
  if prueba:
    mem_cache = Cache(PRUEBA)
  else:
    mem_cache = Cache(CRYS)
  mem_cache.resolver()


if __name__ == '__main__':
  run()

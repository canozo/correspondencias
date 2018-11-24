# Correspondencia Directa

LINEAS = 16
CACHE = 8

PRUEBA = {
  10: ['100-122', '1045-1066'],
  20: ['1052-1070', '2055-2072']
}

CRYS = {
  13: ['7112-7182', '5128-5159'],
  15: ['5138-5208', '13652-13702']
}

class Linea:
  def __init__(self, disponible, num_linea=0, desde=0, hasta=0, size=LINEAS):
    self.size = size
    self.num_linea = num_linea
    self.disponible = disponible
    self.desde = desde
    self.hasta = hasta

  def existe(self, valor):
    return self.desde <= valor <= self.hasta


class Cache:
  def __init__(self, entrada, size=CACHE, size_lineas=LINEAS):
    self.lineas = [Linea(True, num_linea=x, size=size_lineas) for x in range(size)]
    self.entrada = entrada
    self.size = size
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
      result += f'{i} | disp: {linea.disponible}\t| {linea.desde}\t{linea.hasta}\n'
    return result

  def existe_en_cache(self, valor):
    for linea in self.lineas:
      if linea.existe(valor):
        return True
    return False

  def agregar_linea(self, desde, hasta, pos):
    print(self)
    # agregar una linea en la pos de linea
    self.lineas[pos] = Linea(False, desde=desde, hasta=hasta)

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
          linea = bloque % self.size
          fin_bloque = self.size_lineas * bloque + self.size_lineas - 1

          if self.existe_en_cache(desde):
            # ya esta en la cache
            aciertos += 1

          else:
            # no esta en la cache
            # la ingresamos en la linea
            self.agregar_linea(bloque * self.size_lineas, fin_bloque, linea)

            # falla una vez porque no esta en cache
            fallos += 1

          # nos movemos a la siguiente palabra
          desde += 1

        self.lecturas[i] -= 1

    print(self)

    porcentaje = (aciertos / (aciertos + fallos)) * 100
    print(f'Aciertos: {aciertos}\nFallos: {fallos}\nPorcentaje de aciertos: {porcentaje}%')


def run(prueba=True):
  if prueba:
    mem_cache = Cache(PRUEBA)
  else:
    mem_cache = Cache(CRYS)
  mem_cache.resolver()


if __name__ == '__main__':
  run()

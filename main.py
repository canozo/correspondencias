if __name__ == '__main__':
  print('1) Directa')
  print('2) Asociativa secuencial')
  print('3) Asociativa por conjuntos secuencial')
  print('4) LRU')

  opcion = input('[1-4]: ')

  if opcion == '1':
    from utils.directa import *

  elif opcion == '2':
    from utils.asociativa_secuencial import *

  elif opcion == '3':
    from utils.asociativa_conjuntos_secuencial import *

  elif opcion == '4':
    from utils.lru import *

  if opcion in ('1', '2', '3', '4'):
    run(prueba=False)
  else:
    print('Opcion no valida.')
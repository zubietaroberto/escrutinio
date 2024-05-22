from escrutinio.types import Resultado, TipoDeSeleccion, VotoIndividual

def residuos(votos_individuales: list[VotoIndividual], ya_electos: list[Resultado], total_curules: int):
  """Dado un listado de votos individuales, selecciona los diputados por residuo"""
  result: list[Resultado] = []
  partidos_con_residuo = []

  # Sort by votes
  votos_individuales = sorted(votos_individuales, key=lambda x: x.votos, reverse=True)

  for voto in votos_individuales:
    # Si ya se han seleccionado todos los diputados, se termina
    if (len(result) + len(ya_electos) >= total_curules):
      break

    # Si el candidato está ya seleccionado, no se considera
    should_skip = False
    for seleccionado in ya_electos:
      if seleccionado.partido == voto.partido and seleccionado.nombre == voto.nombre:
        should_skip = True
    if should_skip:
      continue

    # Si el partido ya tiene una curul por residuo, no se considera
    if voto.partido in partidos_con_residuo:
      continue
    result.append(Resultado(voto.nombre, voto.partido, voto.votos, TipoDeSeleccion.RESIDUO))
    partidos_con_residuo.append(voto.partido)
  return result
import pandas as pd
from escrutinio.types import VotoIndividual
from constants.coaliciones import coaliciones

def _coalicion_de_partido() -> dict[int, int]:
  """Mapea cada id de partido al id de la coalición a la que pertenece, si tiene una"""
  return {
    partido_id: coalicion.coalicionId
    for coalicion in coaliciones.values()
    for partido_id in coalicion.partidos
  }

def escrutinio_individual(escrutinio: pd.DataFrame):
  """Dado el segundo escrutinio, cuenta todos los votos de todos los cantidatos"""
  result: list[VotoIndividual] = []
  coalicion_de_partido = _coalicion_de_partido()

  # Separar los votos "R" para sumarlos después, agrupados por candidato y coalición.
  # Agrupar solo por nombre mezclaría los votos de dos candidatos homónimos que
  # pertenecen a coaliciones distintas (ver "Known bug" en el README).
  votos_r = escrutinio[escrutinio['Es R']].copy()
  votos_r['Coalicion'] = votos_r['Partido'].map(coalicion_de_partido)
  votos_de_coalicion = votos_r.groupby(['Nombre', 'Coalicion'])['Votos'].sum().to_dict()

  # A todos los votos no "R", agregarlos al arreglo y sumarles los "R"s de su misma coalición
  for _, fila in escrutinio[~escrutinio['Es R']].iterrows():
    votos = fila['Votos']
    is_coalition = False

    # Si le detectamos votos de coalición de la misma coalición a la que pertenece, sumarlos
    coalicion = coalicion_de_partido.get(fila['Partido'])
    clave = (fila['Nombre'], coalicion)
    if coalicion is not None and clave in votos_de_coalicion:
      votos += votos_de_coalicion[clave]
      is_coalition = True

    result.append(
      VotoIndividual(
        partido = fila['Partido'],
        nombre = fila['Nombre'],
        votos = votos,
        is_coalition = is_coalition
      )
    )
  return result

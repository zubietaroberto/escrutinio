import pandas as pd
from escrutinio.types import VotoIndividual

def escrutinio_individual(escrutinio: pd.DataFrame):
  """Dado el segundo escrutinio, cuenta todos los votos de todos los cantidatos"""
  result: list[VotoIndividual] = []
  
  # Separar los votos "R" para sumarlos después. Son de coalición
  votos_de_coalicion: dict[str, int] = {}
  for i, celda in escrutinio[escrutinio['Es R'] == True].iterrows():
    if celda['Nombre'] not in votos_de_coalicion:
      votos_de_coalicion[celda['Nombre']] = 0
    votos_de_coalicion[celda['Nombre']] += celda['Votos']

  # A todos los votos no "R", agregarlos al arreglo y sumarles los "R"s
  for j, celda in escrutinio[escrutinio['Es R'] == False].iterrows():
    votos = celda['Votos']
    is_coalition = False

    # Si le detectamos votos de coalición, sumarlos
    if celda['Nombre'] in votos_de_coalicion:
      votos += votos_de_coalicion[celda['Nombre']]
      is_coalition = True

    result.append(
      VotoIndividual(
        partido = celda['Partido'],
        nombre = celda['Nombre'],
        votos = votos,
        is_coalition = is_coalition
      )
    )
  return result
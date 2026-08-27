import pandas as pd
from escrutinio.types import VotoIndividual

def escrutinio_individual(escrutinio: pd.DataFrame):
  """Dado el segundo escrutinio, cuenta todos los votos de todos los cantidatos"""
  result: list[VotoIndividual] = []

  # Separar los votos "R" para sumarlos después. Son de coalición
  votos_r = escrutinio[escrutinio['Es R']]
  votos_de_coalicion = votos_r.groupby('Nombre')['Votos'].sum().to_dict()

  # A todos los votos no "R", agregarlos al arreglo y sumarles los "R"s
  for _, fila in escrutinio[~escrutinio['Es R']].iterrows():
    votos = fila['Votos']
    is_coalition = False

    # Si le detectamos votos de coalición, sumarlos
    if fila['Nombre'] in votos_de_coalicion:
      votos += votos_de_coalicion[fila['Nombre']]
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
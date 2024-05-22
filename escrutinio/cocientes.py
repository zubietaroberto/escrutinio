import math
import pandas as pd
from escrutinio.types import NominasAsignadas, Resultado, TipoDeSeleccion
from constants.partidos import partidos

# Nombres de los partidos
def nombre_del_partido(id):
  partido = partidos.get(int(id))
  return partido.siglas if partido else id

def nominas_con_curul(primer_escrutinio: pd.DataFrame, curules: int):
  """Devuelve las nominas que tienen derecho a una curul por cociente o medicociente"""
  resultado: list[NominasAsignadas] = []
  cociente = math.floor(primer_escrutinio["Votos"].sum() / curules)
  mediocociente = math.floor(cociente / 2)
  print(f"El cociente es {int(cociente)}, el mediocociente es {int(mediocociente)}")

  valores = primer_escrutinio.copy()
  valores["cociente"] = valores["Votos"] / cociente
  valores["mediocociente"] = valores["Votos"] / mediocociente

  # Cociente
  for i, celda in valores.iterrows():
    curules_del_partido = celda["cociente"]

    # Un partido puede sacar más de una curul por cociente
    while curules_del_partido >= 1:
      print(f"Partido {nombre_del_partido(celda["Partido"])} obtiene cociente")
      resultado.append(NominasAsignadas(celda["Partido"], TipoDeSeleccion.COCIENTE))
      curules_del_partido -= 1

  # Medio Cociente
  for i, celda in valores.iterrows():
    # No considerar partidos que ya tienen curul
    if len(list(filter(lambda x: x.partido == celda["Partido"], resultado))) > 0:
      print(f"Partido {nombre_del_partido(celda["Partido"])} ya tiene curul. No compite por medio cociente.")
      continue

    if celda['mediocociente'] >= 1:
      print(f"Partido {nombre_del_partido(celda["Partido"])} obtiene mediocociente")
      resultado.append(NominasAsignadas(celda["Partido"], TipoDeSeleccion.MEDIOCOCIENTE))
  return resultado

def seleccion_de_curul(curules_asignadas: list[NominasAsignadas], segundo_escrutinio: pd.DataFrame):
  """Dado un listado de partidos, selecciona un candidato por partido"""
  result: list[Resultado] = []
  for curul_asignada in curules_asignadas:
    listado = segundo_escrutinio[segundo_escrutinio['Partido'] == curul_asignada.partido]

    # Candidatos "R" no pueden ser electos por cociente o media cociente
    listado = listado[listado['Es R'] != True]

    # Si el candidato ya está seleccionado, descartarlo
    listado = listado[~listado['Nombre'].isin(list(map(lambda x: x.nombre, result)))]

    # Edge Case: nómina no tiene más candidatos
    if listado.empty:
      continue

    listado.sort_values(by=['Votos'], ascending=False, inplace=True)
    selected = listado.iloc[0]

    result.append(Resultado(selected['Nombre'], curul_asignada.partido, selected['Votos'], curul_asignada.tipo))
  return result
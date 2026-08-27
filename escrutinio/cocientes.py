import math
import pandas as pd
from escrutinio.types import NominasAsignadas, Resultado, TipoDeSeleccion
from constants.partidos import partidos

def nombre_del_partido(partido_id):
  """Devuelve las siglas del partido dado su id"""
  partido = partidos.get(int(partido_id))
  return partido.siglas if partido else partido_id

def nominas_con_curul(primer_escrutinio: pd.DataFrame, curules: int):
  """Devuelve las nominas que tienen derecho a una curul por cociente o medicociente"""
  resultado: list[NominasAsignadas] = []
  cociente = math.floor(primer_escrutinio["Votos"].sum() / curules)
  mediocociente = math.floor(cociente / 2)
  print(f"El cociente es {int(cociente)}, el mediocociente es {int(mediocociente)}")

  valores = primer_escrutinio.copy()
  valores["curules_por_cociente"] = valores["Votos"] / cociente
  valores["curules_por_mediocociente"] = valores["Votos"] / mediocociente

  # Cociente
  for _, fila in valores.iterrows():
    curules_del_partido = fila["curules_por_cociente"]

    # Un partido puede sacar más de una curul por cociente
    while curules_del_partido >= 1:
      print(f"Partido {nombre_del_partido(fila['Partido'])} obtiene cociente")
      resultado.append(NominasAsignadas(fila["Partido"], TipoDeSeleccion.COCIENTE))
      curules_del_partido -= 1

  # Medio Cociente
  for _, fila in valores.iterrows():
    # No considerar partidos que ya tienen curul
    if any(nomina.partido == fila["Partido"] for nomina in resultado):
      print(f"Partido {nombre_del_partido(fila['Partido'])} ya tiene curul. No compite por medio cociente.")
      continue

    if fila["curules_por_mediocociente"] >= 1:
      print(f"Partido {nombre_del_partido(fila['Partido'])} obtiene mediocociente")
      resultado.append(NominasAsignadas(fila["Partido"], TipoDeSeleccion.MEDIOCOCIENTE))
  return resultado

def seleccion_de_curul(curules_asignadas: list[NominasAsignadas], segundo_escrutinio: pd.DataFrame):
  """Dado un listado de partidos, selecciona un candidato por partido"""
  result: list[Resultado] = []
  for curul_asignada in curules_asignadas:
    listado = segundo_escrutinio[segundo_escrutinio['Partido'] == curul_asignada.partido]

    # Candidatos "R" no pueden ser electos por cociente o media cociente
    listado = listado[~listado['Es R']]

    # Si el candidato ya está seleccionado, descartarlo
    nombres_seleccionados = [r.nombre for r in result]
    listado = listado[~listado['Nombre'].isin(nombres_seleccionados)]

    # Edge Case: nómina no tiene más candidatos
    if listado.empty:
      continue

    listado = listado.sort_values(by=['Votos'], ascending=False)
    selected = listado.iloc[0]

    result.append(Resultado(selected['Nombre'], curul_asignada.partido, selected['Votos'], curul_asignada.tipo))
  return result

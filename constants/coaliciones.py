from dataclasses import dataclass

@dataclass
class Coalicion:
  coalicionId: int
  nombre: str
  partidos: list[int]

"""
Sources:
  - Nombres: Wikipedia: https://es.wikipedia.org/wiki/Elecciones_generales_de_Panam%C3%A1_de_2024
  - CoalicionID: Listado completo de postulaciones en CSV
  - Partidos: PDF Handbook given by the Electoral Tribunal of Panama
"""
coaliciones: dict[int, Coalicion] = {
  7: Coalicion(7, nombre="Vamos con Todo", partidos=[2, 4]),
  8: Coalicion(8, nombre="Salvar a Panamá", partidos=[51, 56]),
  9: Coalicion(9, nombre="Lo Bueno Viene", partidos=[8, 32])
}
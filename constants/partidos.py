from dataclasses import dataclass


@dataclass
class Partido:
  partidoId: int
  siglas: str
  descripcion: str

"""
Source: PDF Handbook given by the Electoral Tribunal of Panama
"""
partidos: dict[int, Partido] = {
  2: Partido(2, 'PRD', 'Partido Revolucionario Democrático'),
  3: Partido(3, 'POPULAR', 'Partido Popular'),
  4: Partido(4, 'MOLIRENA', 'Movimiento Liberal Republicano Nacionalista'),
  8: Partido(8, 'PAN', 'Partido Panameñista'),
  32: Partido(32, 'CD', 'Cambio Democrático'),
  51: Partido(51, 'ALIANZA', 'Partido Alianza'),
  52: Partido(52, 'PAIS', 'Partido Alternativa Independiente Social'),
  53: Partido(53, 'MOCA', 'Movimiento Otro Camino'),
  56: Partido(56, 'RM', 'Partido Realizando Metas'),
  57: Partido(57, 'LP1', 'LIbre Postulación 1'),
  58: Partido(58, 'LP2', 'Libre Postulación 2'),
  59: Partido(59, 'LP3', 'Libre Postulación 3'),
  99: Partido(99, 'ELEC', 'ELECCIÓN GENERAL DEL 5 DE MAYO DE 2024'),

  #Not in the PDF. May be wrong
  50: Partido(50, 'FAD', 'Frente Amplio por la Democracia'),
}
from dataclasses import dataclass
from enum import Enum

class TipoDeSeleccion(Enum):
  """Representa el tipo de selección de un candidato"""
  COCIENTE = 1
  MEDIOCOCIENTE = 2
  RESIDUO = 3

@dataclass
class NominasAsignadas:
  """Representa las nominas asignadas a un partido por cociente o mediocociente"""
  partido: int
  tipo: TipoDeSeleccion

@dataclass
class Resultado:
  """Representa el resultado de un candidato electo"""
  nombre: str
  partido: int
  votos: int
  tipo: TipoDeSeleccion

@dataclass
class VotoIndividual:
  """Representa el total individual de un candidato"""
  partido: int
  nombre: str
  votos: int
  is_coalition: bool = False

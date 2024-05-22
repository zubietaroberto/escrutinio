from dataclasses import dataclass

@dataclass
class ProvinciaConCircuitoPlurinominal:
  provinciaId: str
  circuitosPlurinominales: list[str]

circuitos_plurinominales: list[ProvinciaConCircuitoPlurinominal] = [
  ProvinciaConCircuitoPlurinominal("1", ["1-1"]),
  ProvinciaConCircuitoPlurinominal("2", ["2-1"]),
  ProvinciaConCircuitoPlurinominal("3", ["3-1"]),
  ProvinciaConCircuitoPlurinominal("4", ["4-1", "4-3"]),
  ProvinciaConCircuitoPlurinominal("8", ["8-2", "8-3", "8-4", "8-5", "8-6"]),
  ProvinciaConCircuitoPlurinominal("9", ["9-1"]),
  ProvinciaConCircuitoPlurinominal("13", ["13-1", "13-4"]),
]

from dataclasses import dataclass
@dataclass
class Point:
    x: float
    y: float
    z: float = 1.0


p = Point(1.5, 2.5)
print(p)
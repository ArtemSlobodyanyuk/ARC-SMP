class BasePlacement:
    def snap(self, x: float, y: float) -> tuple[float, float]:
        """Інтерфейс для snap"""
        raise NotImplementedError


class FreePlacement(BasePlacement):
    def snap(self, x: float, y: float):
        return x, y


class SquareGridPlacement(BasePlacement):
    def __init__(self, grid_size: float = 32.0):
        self.grid_size = grid_size

    def snap(self, x: float, y: float):
        snapped_x = round(x / self.grid_size) * self.grid_size
        snapped_y = round(y / self.grid_size) * self.grid_size
        return snapped_x, snapped_y
class Entity:
    def __init__(self, id: str, x: float = 0.0, y: float = 0.0, props: dict = None):
        self.id = id
        self.x = x
        self.y = y
        self.props = props or {}

    def set_position(self, x: float, y: float):
        self.x = x
        self.y = y
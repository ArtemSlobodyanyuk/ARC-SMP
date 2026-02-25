import os
import json
from red2.logic.scene import Scene
from red2.logic.entity import Entity
from red2.logic.placement import FreePlacement, SquareGridPlacement

class Core:
    def __init__(self, object_path="object", save_path="save"):
        self.object_path = object_path
        self.save_path = save_path
        self.scene = Scene()
        self.placement = FreePlacement()  # дефолтна стратегія
        self.load_objects()

    def load_objects(self):
        """Завантаження шаблонів об’єктів з папки object"""
        for filename in os.listdir(self.object_path):
            if filename.endswith(".json"):
                path = os.path.join(self.object_path, filename)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    entity = Entity(
                        id=data.get("id", filename),
                        x=data.get("x", 0.0),
                        y=data.get("y", 0.0),
                        props=data.get("props", {})
                    )
                    self.scene.add_entity(entity)

    def switch_placement(self, mode: str):
        """Перемикання системи розміщення"""
        if mode == "Free":
            self.placement = FreePlacement()
        elif mode == "SquareGrid":
            self.placement = SquareGridPlacement(grid_size=32)
        else:
            raise ValueError(f"Невідомий режим: {mode}")

    def save_scene(self, filename="demo_map.json"):
        """Збереження сцени у JSON"""
        data = {
            "entities": [
                {"id": e.id, "x": e.x, "y": e.y, "props": e.props}
                for e in self.scene.entities
            ]
        }
        path = os.path.join(self.save_path, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_scene(self, filename):
        """Завантаження сцени з JSON"""
        path = os.path.join(self.save_path, filename)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.scene.clear()
            for e_data in data.get("entities", []):
                entity = Entity(
                    id=e_data.get("id"),
                    x=e_data.get("x", 0.0),
                    y=e_data.get("y", 0.0),
                    props=e_data.get("props", {})
                )
                self.scene.add_entity(entity)
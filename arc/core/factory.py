from arc.items.shapes import CircleItem, SquareItem, RectangleItem


class ObjectFactory:

    def __init__(self, scene):
        self.scene = scene

    def create(self, obj_type):
        if obj_type == "circle":
            obj = CircleItem()
        elif obj_type == "square":
            obj = SquareItem()
        elif obj_type == "rectangle":
            obj = RectangleItem()
        else:
            return

        obj.setPos(200, 200)
        self.scene.addItem(obj)

        return obj

    def create_from_data(self, data: dict):
        """
        Recreate an item from serialized data.
        Expected keys: type, x, y, w, h, name, note.
        """
        obj_type = data.get("type")
        obj = self.create(obj_type)
        if obj is None:
            return None

        # Position/size
        try:
            obj.setPos(float(data.get("x", 0)), float(data.get("y", 0)))
        except Exception:
            pass

        try:
            w = float(data.get("w", obj.rect().width()))
            h = float(data.get("h", obj.rect().height()))
            obj.resize(w, h)
        except Exception:
            pass

        # Properties
        obj.name = str(data.get("name", obj.name))
        obj.note = str(data.get("note", obj.note))

        return obj

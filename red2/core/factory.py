from items.shapes import CircleItem, SquareItem, RectangleItem


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
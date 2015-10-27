import os
import os.path
import yaml

from frames.frame import Frame

class FrameSet:
    def __init__(self, path):
        self.folder = path
        self.frames = {}
        self.todo = {}

    def importFile(self, path):
        with open(path) as file:
            return self.importData(yaml.load(file))

    def importData(self, data):
        if "parent" in data and not data["parent"] in self.frames:
            self.todo[data["name"]] = data
            return None

        self.frames[data["name"]] = Frame.fromData(data)
        if "parent" in data:
            self.frames[data["name"]].setParent(self.frames[data["parent"]])

        if data["name"] in self.todo:
            self.todo.pop(data["name"])

        return self.frames[data["name"]]

    def importAll(self):
        files = os.listdir(self.folder)
        for name in files:
            if name.startswith("."):
                continue
            self.importFile(os.path.join(self.folder, name))

        end = 50
        while len(self.todo):
            end -= 1
            if end <= 0:
                raise RuntimeError("No se resuelven nunca las dependencias de los padres!")

            for v in [x for x in self.todo.values()]:
                self.importData(v)


    def toString(self):
        lines = []
        for k, v in self.frames.items():
            lines.append("%s" % v)
        return "\n".join(lines)

    def __repr__(self):
        return self.toString()

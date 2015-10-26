import os
import os.path
import yaml

from frames.frame import Frame

class FrameSet:
    def __init__(self, path):
        self.folder = path
        self.frames = {}
        self.todo = {}

    def importFile(self, data):
        if "parent" in data and not data["parent"] in self.frames:
            self.todo[data["name"]] = data
            return

        self.frames[data["name"]] = Frame(data["name"])
        if "parent" in data:
            self.frames[data["name"]].setParent(self.frames[data["parent"]])

        self.frames[data["name"]].setValues(data["data"])

        if data["name"] in self.todo:
            self.todo.pop(data["name"])

    def importAll(self):
        files = os.listdir(self.folder)
        for name in files:
            if name.startswith("."):
                continue
            with open(os.path.join(self.folder, name)) as file:
                self.importFile(yaml.load(file))

        end = 50
        while len(self.todo):
            end -= 1
            if end <= 0:
                raise SyntaxError("No se resuelven nunca las dependencias de los padres!")

            for k, v in self.todo.items():
                self.importFile(v)


    def toString(self):
        lines = []
        for k, v in self.frames.items():
            lines.append("%s" % v)
        return "\n".join(lines)

    def __repr__(self):
        return self.toString()

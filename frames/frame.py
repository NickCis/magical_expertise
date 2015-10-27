import os.path
import yaml

class Frame:
    def __init__(self, name):
        self.parent = None
        self.data = {}
        self.columns = []
        self.name = name

    def getColumns(self):
        cols = [] + self.columns
        if self.parent:
            for v in self.parent.getColumns():
                if v not in cols:
                    cols.append(v)
        return cols

    def setParent(self, parent):
        self.parent = parent

    def getValue(self, col):
        if not col in self.getColumns():
            return None

        if col in self.data:
            return self.data[col]

        if self.parent:
            return self.parent.getValue(col)

    def setValue(self, col, val):
        self.data[col] = val;
        if not col in self.columns:
            self.columns.append(col)

    def setValues(self, vals):
        if type(vals) == dict:
            for key, value in vals.items():
                self.setValue(key, value)
        elif type(vals) == list:
            for v in vals:
                self.setValues(v)
        else:
            self.setValue(vals, "")

    def toString(self):
        lines = ["----", self.name]
        for col in self.getColumns():
            lines.append("%s: %s" % (col, self.getValue(col)))

        return "\n".join(lines);

    def __repr__(self):
        return self.toString()

    @staticmethod
    def fromFile(path):
        with open(path) as file:
            return Frame.fromData(yaml.load(file))

    @staticmethod
    def fromData(data):
        frame = Frame(data["name"])
        frame.setValues(data["data"])
        return frame


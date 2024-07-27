class Cell:
    def __init__(self, frame, ID, xmin, ymin, xmax, ymax, remove, x, y, velocity):
        self.frame = frame
        self.ID = ID
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.remove = remove
        self.x = x
        self.y = y
        self.velocity = velocity

    def __repr__(self):
        return (f"Cell(frame={self.frame}, ID={self.ID}, xmin={self.xmin}, ymin={self.ymin}, "
                f"xmax={self.xmax}, ymax={self.ymax}, remove={self.remove}, x={self.x}, "
                f"y={self.y}, velocity={self.velocity})")

    def to_dict(self):
        return {
            'frame': self.frame,
            'ID': self.ID,
            'xmin': self.xmin,
            'ymin': self.ymin,
            'xmax': self.xmax,
            'ymax': self.ymax,
            'remove': self.remove,
            'x': self.x,
            'y': self.y,
            'velocity': self.velocity
        }

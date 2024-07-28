import math

class Frame:
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
        return (f"Frame(frame={self.frame}, ID={self.ID}, xmin={self.xmin}, ymin={self.ymin}, "
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

class Cell:
    def __init__(self, initial_frame_info):
        """
        Initialize the Cell with the first frame information.
        initial_frame_info should be a dictionary containing the cell's information in the first frame.
        """
        self.frames = [Frame(**initial_frame_info)]

    def __repr__(self):
        """
        Represent the Cell with all its frame information.
        """
        return f"Cell(frames={self.frames})"

    def to_dict(self):
        """
        Convert the Cell to a dictionary with all its frame information.
        """
        return {'frames': [frame.to_dict() for frame in self.frames]}

    def add_frame_info(self, frame_info):
        """
        Add information for a new frame to the Cell.
        frame_info should be a dictionary containing the cell's information in the new frame.
        """
        self.frames.append(Frame(**frame_info))

    def distance_to(self, other, frame_index=-1):
        """
        Calculate the distance to another cell based on the specified frame index.
        Defaults to the latest frame if frame_index is not provided.
        """
        x1, y1 = self.frames[frame_index].x, self.frames[frame_index].y
        x2, y2 = other.frames[frame_index].x, other.frames[frame_index].y
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    @staticmethod
    def find_nearest(current_cell, next_frame_cells, frame_index=-1):
        """
        Find the nearest cell in the next frame based on the specified frame index.
        Defaults to the latest frame if frame_index is not provided.
        """
        nearest_cell = None
        min_distance = float('inf')

        for cell in next_frame_cells:
            distance = current_cell.distance_to(cell, frame_index)
            if distance < min_distance:
                min_distance = distance
                nearest_cell = cell

        return nearest_cell
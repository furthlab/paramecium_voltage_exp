from cell import Cell
import pandas as pd


def main():
    # Sample data in dictionary form to simulate a CSV file load
    data = [
        {'frame': 1, 'ID': 1, 'xmin': 10, 'ymin': 20, 'xmax': 30, 'ymax': 40, 'remove': False, 'x': 20, 'y': 30,
         'velocity': 5},
        {'frame': 2, 'ID': 1, 'xmin': 15, 'ymin': 25, 'xmax': 35, 'ymax': 45, 'remove': False, 'x': 25, 'y': 35,
         'velocity': 5},
        {'frame': 1, 'ID': 2, 'xmin': 50, 'ymin': 60, 'xmax': 70, 'ymax': 80, 'remove': False, 'x': 60, 'y': 70,
         'velocity': 3},
        {'frame': 2, 'ID': 2, 'xmin': 55, 'ymin': 65, 'xmax': 75, 'ymax': 85, 'remove': False, 'x': 65, 'y': 75,
         'velocity': 3},
        {'frame': 2, 'ID': 3, 'xmin': 100, 'ymin': 110, 'xmax': 120, 'ymax': 130, 'remove': False, 'x': 110, 'y': 120,
         'velocity': 2}
    ]

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Dictionary to hold Cell objects indexed by their ID
    cells_dict = {}

    # Group data by frame to ensure chronological order of frames
    grouped = df.groupby('frame')

    # Iterate through each frame's data
    for frame_id, group in grouped:
        for _, row in group.iterrows():
            cell_info = {
                'frame': row['frame'],
                'ID': row['ID'],
                'xmin': row['xmin'],
                'ymin': row['ymin'],
                'xmax': row['xmax'],
                'ymax': row['ymax'],
                'remove': row['remove'],
                'x': row['x'],
                'y': row['y'],
                'velocity': row['velocity']
            }

            if row['ID'] in cells_dict:
                # Add frame information to the existing Cell object
                cells_dict[row['ID']].add_frame_info(cell_info)
            else:
                # Create a new Cell object with the initial frame information
                cells_dict[row['ID']] = Cell(cell_info)

    # Example: Find the nearest cell in the next frame for a given cell in the current frame
    current_frame_id = 1
    next_frame_id = current_frame_id + 1

    # Group cells by frame
    cells_by_frame = {}
    for cell in cells_dict.values():
        for frame in cell.frames:
            frame_id = frame.frame
            if frame_id not in cells_by_frame:
                cells_by_frame[frame_id] = []
            cells_by_frame[frame_id].append(cell)

    if current_frame_id in cells_by_frame and next_frame_id in cells_by_frame:
        current_frame_cells = cells_by_frame[current_frame_id]
        next_frame_cells = cells_by_frame[next_frame_id]

        # Assuming we want to find the nearest cell for the first cell in the current frame
        current_cell = current_frame_cells[0]
        nearest_cell = Cell.find_nearest(current_cell, next_frame_cells)

        if nearest_cell:
            print(
                f"The nearest cell to {current_cell.frames[-1]} in frame {next_frame_id} is {nearest_cell.frames[-1]}")
        else:
            print(f"No cells found in frame {next_frame_id}")
    else:
        print(f"Frames {current_frame_id} or {next_frame_id} not found in the data.")


if __name__ == "__main__":
    main()

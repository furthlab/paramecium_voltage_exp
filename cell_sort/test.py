import os

from cell import Cell
import pandas as pd

def load_data_from_csv():
    """
    Load data from a list of CSV files and return a dictionary of DataFrames.

    Parameters:
    filenames (list of str): List of file paths to the CSV files.

    Returns:
    dict: Dictionary where the keys are file names and values are DataFrames.
    """
    # Example usage with the given files
    print(os.getcwd())
    file_paths = [
        'example_group/frame_2.csv',
        'example_group/frame_3.csv',
        'example_group/frame_4.csv',
        'example_group/frame_5.csv',
        'example_group/frame_6.csv',
        'example_group/frame_7.csv',
        'example_group/frame_8.csv',
        'example_group/frame_9.csv'
    ]
    data_frames = {}
    for file in file_paths:
        try:
            df = pd.read_csv(file)
            data_frames[file] = df
        except Exception as e:
            print(f"Error loading {file}: {e}")
    return data_frames

def main():
    # Sample data in dictionary form to simulate a CSV file load
    data = load_data_from_csv()

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

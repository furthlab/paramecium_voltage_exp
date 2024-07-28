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

    combined_df = pd.concat(data, ignore_index=True)
    # Group data by frame to ensure chronological order of frames
    grouped = combined_df.groupby('frame')

    print(grouped.head())

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

    current_frame_id = 1
    next_frame_id = current_frame_id + 1

if __name__ == "__main__":
    main()

import csv
import re
import json
import tqdm
import os
import os.path as osp
import argparse
import glob
import logging
import time
import os
import re

def logger_setup():
    """ logger_setup

    Returns:
        : logger
    """
    # create logger
    logger = logging.getLogger('Split into each frame')
    logger.setLevel(logging.CRITICAL)
    # create file handler which logs even debug messages
    log_name = '../log/{}.log'.format(time.strftime('%Y-%m-%d-%H-%M'))
    fh = logging.FileHandler(log_name)
    fh.setLevel(logging.CRITICAL)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.disabled = True  # Disable the logger
    return logger

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, default='../processed',help='directory of to be split files', dest='input_dir')
    parser.add_argument('--split-dir', type=str, default='../split_frame',help='directory to split files', dest='split_dir')
    return parser.parse_args()


def group_by_concept_type(data, number_of_concept_type):
    number_of_concept_type = int(number_of_concept_type)
    list_of_empty_lists = [[] for _ in range(number_of_concept_type)]

    for entry in data:
        concept_type = entry.get('concept_type')
        if concept_type is not None:
            try:
                concept_type_index = int(concept_type)
                if 0 <= concept_type_index < number_of_concept_type:
                    list_of_empty_lists[concept_type_index].append(entry)
                else:
                    print(f"Skipping entry with invalid concept_type (out of range): {concept_type} in entry {entry}")
            except ValueError:
                print(f"Skipping entry with non-integer concept_type: {concept_type} in entry {entry}")
        else:
            print(f"Skipping entry with no concept_type found: {entry}")

    return list_of_empty_lists


def save_lists_to_files(list_of_lists, output_path):
    os.makedirs(output_path, exist_ok=True)
    for i, lst in enumerate(list_of_lists):
        file_name = os.path.join(output_path, f'concept_{i}.json')
        with open(file_name, 'w') as f:
            json.dump(lst, f, indent=4)
        print(f'Saved concept {i} to {file_name}')

if __name__ == "__main__":
    args = get_args()
    print(os.getcwd())
    out_path = args.filtered_dir
    input_path = args.json_dir
    json_data = []
    number_of_concept = args.concept_number

    for filename in os.listdir(input_path):
        if filename.endswith('.json'):
            filepath = os.path.join(input_path, filename)
            with open(filepath, 'r') as file:
                try:
                    data = json.load(file)
                    json_data.append(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {filepath}: {e}")

    merge = []
    for data in json_data:
        merge = merge + data

    split_data = group_by_concept_type(merge, number_of_concept)
    save_lists_to_files(split_data, out_path)
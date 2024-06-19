import argparse
import os
from main import process


def list_all_files(directory, extension):
    """
    List all files with the given extension in a directory.

    :param directory: directory to list
    :param extension: file extension
    """
    res = []
    for root, dirs, files in os.walk(directory):
        files.sort()
        for file in files:
            # check that it is a file with the correct extension
            if len(file) >= 3 and file[-len(extension)::] == extension:
                res.append(os.path.join(root, file))
    res.sort()
    return res

def main(data_dir):
    res = list_all_files(data_dir, '.jpg')
    for s in res:
        print(s)
    print(process(res[0]))



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="path to the data folder")
    args = parser.parse_args()

    main(args.data)


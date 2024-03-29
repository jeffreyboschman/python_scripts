import os
import pathlib
import argparse


def main(files_textfile, input_dir):
    file_list = read_data_ids(files_textfile)
    for cur_file in file_list:
        input_path = os.path.join(input_dir, cur_file)
        try:
            bash_command = 'rm ' + input_path
            os.system(bash_command)
            print(bash_command)
        except Exception as e:
            print(e)
            print(f"{input_path} was not removed properly")


def read_data_ids(data_id_path):
    with open(data_id_path) as file:
        data_ids = file.readlines()
        data_ids = [x.strip() for x in data_ids]
    return data_ids

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''For removing certain files''')

    parser.add_argument('--files_textfile', type=str, required=True,
            help='the path to a textfile that contains lines with the file ids')
    parser.add_argument('--input_dir', type=str, required=True,
            help='the path to the root dir where the original file are saved')

    args = parser.parse_args()

    main(args.files_textfile, args.input_dir) 

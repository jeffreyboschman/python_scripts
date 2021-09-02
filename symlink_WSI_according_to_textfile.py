from tqdm import tqdm
import os
import pathlib
import argparse


def main(WSI_id_textfile, input_dir, output_dir):
    WSI_list = read_data_ids(WSI_id_textfile)
    ensure_directory_exists(output_dir)
    for WSI in WSI_list:
        input_path = os.path.join(input_dir, WSI)
        output_path = os.path.join(output_dir, WSI)
        try:
            bash_command = 'ln -s "' + input_path +'" "' + output_path + '"'
            os.system(bash_command)
        except Exception as e:
            print(e)
            print(f"{input_path} was not symlinked properly")


def read_data_ids(data_id_path):
    with open(data_id_path) as file:
        data_ids = file.readlines()
        data_ids = [x.strip() for x in data_ids]
    return data_ids

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''For symlinking certain WSIs''')

    parser.add_argument('--WSI_id_textfile', type=str, required=True,
            help='the path to a textfile that contains lines with the WSI ids')
    parser.add_argument('--input_dir', type=str, required=True,
            help='the path to the root dir where the original WSI images are saved')
    parser.add_argument('--output_dir', type=str, required=True,
            help='the path to the root dir where you want the symlinks to be')

    args = parser.parse_args()

    main(args.WSI_id_textfile, args.input_dir, args.output_dir) 

import os
import argparse

def get_patch_ids(path_in, patch_ids_outfile):
    with open(patch_ids_outfile, 'w') as out_file:
        for r, d, f in os.walk(path_in):
            for filename in f:
                if '.png' in filename:
                    relative_dir = os.path.relpath(r, path_in)
                    file_no_ending = filename.split('.')[0]
                    out_file.write("%s\n" % os.path.join(relative_dir, file_no_ending))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''For getting a textfile containing patch ids from all the png files saved in the directory tree format of the patch ids''')

    parser.add_argument('--path_in', type=str, required=True, help='The full path to a directory where the subtypes are listed, perhaps')
    parser.add_argument('--patch_ids_outfile', type=str, required=True, help='The full path to a textfile you want written that will contain the patch ids')

    args = parser.parse_args()

    get_patch_ids(args.path_in, args.patch_ids_outfile)

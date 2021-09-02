from tqdm import tqdm
import os
import argparse

def read_data_ids(data_id_path):
    """Function to read data ids (i.e., any *.txt contains row based information)

    Parameters
    ----------
    data_id_path : string
        Absoluate path to the *.txt contains data ids

    Returns
    -------
    data_ids : list
        List conntains data ids

    """
    with open(data_id_path) as file:
        data_ids = file.readlines()
        data_ids = [x.strip() for x in data_ids]
    return data_ids

def symlink_pngs_from_list(patch_ids_file, input_dir, output_dir):

    patch_ids = read_data_ids(patch_ids_file)

    count = 0 

    for patch_id in tqdm(patch_ids):
        #assumes patch_id has the form: subtype/WSI_id/coordinates
        subtype_id = patch_id.split('/')[0]
        WSI_id = patch_id.split('/')[1]
        coordinates_id = patch_id.split('/')[2]
        image_name = coordinates_id + '.png'
        image_path = os.path.join(input_dir, subtype_id, WSI_id, image_name)
        image_out_path = os.path.join(output_dir, subtype_id, WSI_id, image_name)
        out_directory = os.path.join(output_dir, subtype_id, WSI_id)
        os.makedirs(out_directory, exist_ok=True)
        try: 
            bash_command = "ln -s \""+image_path+"\" \""+image_out_path+"\""
            os.system(bash_command)
            count += 1
        except:
            print("The following images were not symlinked properly:", image_name)


    print('Number of patches symlinked:', count)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''For creating an h5 file containing all the pngs specified by a textfile''')

    parser.add_argument('--patch_ids', type=str, required=True,
            help='the path to a textfile that contains lines with the patch ids, ex. CC/VOA-113/11243_52134')
    parser.add_argument('--input_dir', type=str, required=True,
            help='the path to the root dir where the original png images are saved')
    parser.add_argument('--output_dir', type=str, required=True,
            help='the path to the root dir where you want the symlinks to be')

    args = parser.parse_args()

    symlink_pngs_from_list(args.patch_ids, args.input_dir, args.output_dir) 

import h5py
import numpy as np
from tqdm import tqdm
from PIL import Image
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

def create_h5_from_png(h5py_file, patch_ids_file, input_dir, patch_id_suffix, set_storage_names, augmentation=False):

    print('creating file:', h5py_file)

    patch_ids = read_data_ids(patch_ids_file)

    count = 0 
    for i, storage_name in enumerate(set_storage_names):
        with h5py.File(h5py_file,'a') as f:
            for patch_id in tqdm(patch_ids):
                subtype_id = patch_id.split('/')[0]
                WSI_id = patch_id.split('/')[1]
                coordinates_id = patch_id.split('/')[2]
                image_name = coordinates_id + patch_id_suffix[i] + '.png'
                image_path = os.path.join(input_dir, subtype_id, WSI_id, image_name)
                if augmentation:
                    suffix = patch_id.split('/')[3]
                    image_name = suffix + '.png'
                    image_path = os.path.join(input_dir, subtype_id, WSI_id, coordinates_id, image_name)
                cur_image = np.asarray(Image.open(image_path))
                store_name = storage_name
                if augmentation:
                    store_name = suffix
                grp = f.require_group(subtype_id +'/'+ WSI_id +'/'+ coordinates_id)
                if store_name in list(grp.keys()):
                    del grp[store_name]
                grp.create_dataset(store_name, data=cur_image)
                count += 1

    print('Number of patches in h5 file:', count)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''For creating an h5 file containing all the pngs specified by a textfile''')

    parser.add_argument('--h5py_file', type=str, required=True,
            help='the path to an h5py file that will contain the patches as h5py dataset objects, ex. f["CC/VOA-113/11243_52134/image_data"]')
    parser.add_argument('--patch_ids', type=str, required=True,
            help='the path to a textfile that contains lines with the patch ids, ex. CC/VOA-113/11243_52134')
    parser.add_argument('--input_dir', type=str, required=True,
            help='the path to where the png images are saved')
    parser.add_argument('--patch_id_suffix', nargs='+', type=str, help='the suffix after the coordinates that all the patches you want are saved as. ex. if the patches are saved as "12456_12342_vahadane_EC+VOA-1515+52341_32342", input "_vahadane_EC+VOA-1515+52341_32342". For a list, input all the arguments with spaces in between. Ex. "_vahadane_EC" "_vahadane_MC" _vahadane "HGSC". For nothing, input ""')
    parser.add_argument('--set_storage_name', nargs='+',  type=str,  help='an optional storage name that will be the name of every patch stored in the h5 file. ex: "vahadane_EC+VOA-1515+52341_32342". For a list, input all the argments with spaces in between. For nothing, input "image_data".')

    parser.add_argument('--augmentation', action='store_true', help='if the patch ids are in the form ex. CC/VOA-113/11243_52134/vahadane_HGSC+VOA-1515A+45234_12338')

    args = parser.parse_args()

    create_h5_from_png(args.h5py_file, args.patch_ids, args.input_dir, args.patch_id_suffix, args.set_storage_name, args.augmentation)
       

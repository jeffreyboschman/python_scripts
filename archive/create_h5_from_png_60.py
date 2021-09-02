import h5py
import numpy as np
from tqdm import tqdm
from PIL import Image
import os

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

input_dir = '/projects/ovcare/classification/jboschman/colour_norm/datasets/zheng/60_dataset/'
id_path = '/projects/ovcare/classification/jboschman/colour_norm/datasets/256_monoscale_20x/patch_ids/150_per_patients_test_patch_ids.txt'
h5filename = '/projects/ovcare/classification/jboschman/colour_norm/datasets/256_monoscale_20x/256_monoscale_20x_60_zheng.h5'
method = 'zheng'
# ref_images = ['EC+VOA-1351B', 'HGSC+VOA-1515A', 'MC+VOA-1179A', 'EC+OOU-6']
ref_images = ['HGSC+VOA-1515A', 'EC+OOU-6']

print('creating file:', h5filename )

ids = read_data_ids(id_path)

count = 0 
subtype_path = ''

with h5py.File(h5filename,'a') as f:
    for line in tqdm(ids):
        grp = f.require_group(line)
        subtype_id = line.split('/')[0]
        image_id = line.split('/')[1]
        patch_id = line.split('/')[2]
        for ref_image in ref_images:
            patch_name = patch_id + '+' + method + '_' + ref_image + '.png'
            image_path = os.path.join(input_dir, subtype_id, image_id, patch_name)
            patch = np.asarray(Image.open(image_path))
            store_name = method + '_' + ref_image
            if store_name in list(grp.keys()):
                del grp[store_name]
            grp.create_dataset(method + '_' + ref_image, data=patch)
            count += 1
print('Number of patches in h5 file:', count)

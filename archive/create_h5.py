import h5py
import openslide
import numpy as np
from tqdm import tqdm
from PIL import Image

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

def extract_and_resize(slide, location_width, location_height, extract_size, resize_size):
    """Function to extract a patch from slide at (location_width, location_height) and then resize
        using Lanczos resampling filter
    Parameters
    ----------
    slide : OpenSlide object
        An numpy array contains a pillow image
    location_width : int
        Patch location width
    location_height : int
        Patch location height
    extract_size : int
        Extract patch size
    resize_size : int
        Resize patch size
    Returns
    -------
    patch : Pillow image
        A resized patch
    """
    patch = slide.read_region(
        (location_width, location_height), 0, (extract_size, extract_size)).convert('RGB')
    if extract_size != resize_size:
        patch = patch.resize((resize_size, resize_size),
                             resample=Image.LANCZOS)
    return patch


WSI_path = '/projects/ovcare/WSI/Dataset_Slides_500_cases/'
id_path = '/projects/ovcare/classification/jboschman/colour_norm/datasets/256_monoscale_20x/patch_ids/300_150_per_patients_1_2_train_3_eval_full_ids.txt'
h5filename = '/projects/ovcare/classification/jboschman/colour_norm/datasets/256_monoscale_20x/256_monoscale_20x_khan.h5'

print('creating file:', h5filename )

ids = read_data_ids(id_path)
original_size = 512
downsample_size = 256

count = 0 
subtype_path = ''

with h5py.File(h5filename,'w') as f:
    for line in tqdm(ids):
        grp = f.create_group(line)
        subtype_id = line.split('/')[0]
        image_id = line.split('/')[1]
        patch_id = line.split('/')[2]
        x = int(patch_id.split('_')[0])
        y = int(patch_id.split('_')[1])
        if subtype_id == 'CC':
            subtype_path = 'clear_cell_carcinoma_100/'
        elif subtype_id == 'EC':
            subtype_path = 'endometrioid_carcinoma_100/'
        elif subtype_id == 'HGSC':
            subtype_path = 'high_grade_serous_carcinoma_300/'
        elif subtype_id =='LGSC': 
            subtype_path = 'low_grade_serous_carcinoma_50/'
        elif subtype_id == 'MC':
            subtype_path = 'mucinous_carcinoma_50/'
        else:
            print('Error at line:', count)
        image_path = WSI_path + subtype_path + image_id + '.tiff'
        WSI = openslide.OpenSlide(image_path)
        patch = extract_and_resize(WSI, x, y, original_size, downsample_size)
        patch = np.array(patch) #type int
        WSI.close() 
        grp.create_dataset('image_data', data=patch)
        count += 1
print('Number of patches in h5 file:', count)

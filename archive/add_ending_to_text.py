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

id_path = '/projects/ovcare/classification/jboschman/colour_norm/datasets/256_monoscale_20x/patch_ids/300_150_per_patients_1_2_train_3_eval_train_ids.txt'
new_file = '/projects/ovcare/classification/jboschman/colour_norm/datasets/256_monoscale_20x/patch_ids/300_150_per_patients_1_2_train_3_eval_train_ids_vahadane_HGSC+VOA-1515A+1024+51200_41984.txt'
ending = 'vahadane_HGSC+VOA-1515A+1024+51200_41984'  #'image_data' #'vahadane_MC+VOA-1179A+1024+38912_56320'  #'vahadane_EC+VOA-1351B+1024+25600_26624'

ids = read_data_ids(id_path)

with open(new_file, 'w') as f:
    for line in ids:
        f.write(line + "/" + ending + "\n")

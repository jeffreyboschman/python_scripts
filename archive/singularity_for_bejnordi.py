import os

ids = ["'VOA-495(A3).tif'", "VOA-5563A.tif"]

for i in ids:
    bash_command = "singularity run aim_images_bejnordi.sif --input /projects/ovcare/classification/jboschman/colour_norm/bejnordi/300_WSI_copies/LGSC/"+i" --image_output /projects/ovcare/classification/jboschman/colour_norm/bejnordi/normalized_WSI/LGSC/ --template_input /projects/ovcare/classification/jboschman/colour_norm/bejnordi/template_HGSC+VOA-1515A.csv --seed 1234"
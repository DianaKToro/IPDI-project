import ants 
import nibabel as nib
import numpy as np
from medpy import metric
from static import config
class Registration:

    def register(flair_img, image, call_methods_seg):
        fixed_img = ants.image_read(config.RESOURCES['imgs'].format(flair_img))
        mixed_img = ants.image_read(config.RESOURCES['imgs'].format(image))
        #fixed_img = ants.from_numpy(flair_img)
        #mixed_img = ants.from_numpy(image)
        registered_img = ants.registration(fixed=fixed_img, moving=mixed_img, type_of_transform = 'SyN' )
        register = registered_img['warpedmovout']
    
        call_methods_seg.mri_image = register

    def calculate_volumes(image):
        image_header = image.header
        pixdim = image_header['pixdim']
        pixel_size = np.prod(pixdim[1:4])

        image_data = image.get_fdata()
        unique_labels = np.unique(image_data.astype(int))

        cluster_volumens = {}
        for label in unique_labels:
            if label == 0:
                continue
        
            cluster_mask = (image_data == label)
            cluster_pixels = np.sum(cluster_mask)
            cluster_volumen = cluster_pixels * pixel_size

            cluster_volumens[label] = cluster_volumen
        print(cluster_volumens)
        return cluster_volumens

    def calculate_metrics(image, image_reference):
        segmentation_data = image.get_fdata()
        reference_data = image.get_fdata()

        dice_score = metric.dc(segmentation_data, reference_data)
        jaccard_index = metric.binary.jc(segmentation_data, reference_data)

        return{
            'Dice Score' : dice_score,
            'Jaccard' : jaccard_index
        }
            

        


from pyrobex.robex import robex
import nibabel as nib
from static import config

class Removal:

    def skullRemoval(image, call_methds_seg):
        
        stripped, mask = robex(image)  
        
        
        call_methds_seg.mri_image = stripped.get_fdata()

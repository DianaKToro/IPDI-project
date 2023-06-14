import numpy as np

class Denoising:

    def mean_filter(image, call_methods_seg):
        depth, height, width = image.shape
        filtered_image = np.zeros_like(image)
        for z in range(1, depth - 1):
            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    neighbors = [
                        image[z-1, y, x],
                        image[z+1, y, x],
                        image[z, y-1, x],
                        image[z, y+1, x],
                        image[z, y, x-1],
                        image[z, y, x+1],
                        image[z, y, x]
                    ]
                    filtered_value = int(np.mean(neighbors))
                    filtered_image[z, y, x] = filtered_value

        call_methods_seg.mri_image = filtered_image

    def median_filter(image, call_methods_seg):
        depth, height, width = image.shape
        filtered_image = np.zeros_like(image)
        for z in range(1, depth - 1):
            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    neighbors = [
                        image[z-1, y, x],
                        image[z+1, y, x],
                        image[z, y-1, x],
                        image[z, y+1, x],
                        image[z, y, x-1],
                        image[z, y, x+1],
                        image[z, y, x]
                    ]
                    filtered_value = int(np.median(neighbors))
                    filtered_image[z, y, x] = filtered_value

        call_methods_seg.mri_image = filtered_image

    def edge_detection(image, call_methods_seg):
        #puede recibir una imagen con remocion de ruido o una imagen sin remocion de ruido
        dfdx = np.zeros_like(image)
        dfdy = np.zeros_like(image)
        dfdz = np.zeros_like(image)
        for z in range(1, image.shape[0] - 2):
            for y in range(1, image.shape[1] - 2):
                for x in range(1, image.shape[2] - 2):
                    dfdx[z,y,x] = image[z+1, y, x]- image[z-1,y,x]
                    dfdy[z,y,x] = image[z, y+1, x]- image[z,y-1,x]
                    dfdz[z,y,x] = image[z, y, x+1]- image[z,y,x-1]
        edge = np.sqrt(np.power(dfdx,2)+np.power(dfdy,2)+np.power(dfdz,2))

        call_methods_seg.mri_image = edge 

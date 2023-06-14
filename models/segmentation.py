import numpy as np

class Segmentation:

    def thresholding(image, tol, tau, call_methods_seg):
        while True:

            thresholding_img = image >= tau
            mBG = image[np.multiply(image > 10, thresholding_img == 0)].mean()
            mFG = image[np.multiply(image > 10, thresholding_img == 1)].mean()

            tau_post = 0.5 * (mBG + mFG)

            if np.abs(tau - tau_post) < tol:
                break
            else:
                tau = tau_post
        call_methods_seg.mri_image = thresholding_img
    
    def get_neighbors(self, matrix, row, col, radius, z_start_layer = 0, z_depth = 0):
        neighbors = []
        for r in range(row - radius, row + radius + 1):
            for c in range(col - radius, col + radius + 1):
                if r == row and c == col:
                    continue
                if r < 0 or r >= len(matrix) or c < 0 or c >= len(matrix[0]):
                    continue
                for z_index in range(z_depth + 1):
                    if abs(r - row) == radius or abs(c - col) == radius:
                        neighbors.append((r, c, z_start_layer + z_index))
        return neighbors

    def regionGrowing(self, image, tol, x, y, z, z_depth, z_layer, call_methods_seg):
        mean_value_cluster = image[x, y, z]
        segmentation = np.zeros_like(image)
        rows_image = image.shape[0]
        radious = 1

        while radious < rows_image:
            neighbors = self.get_neighbors(image, x, y, radious, z_layer, z_depth)
            for neighbor_index in neighbors:
                x_index = neighbor_index[0]
                y_index = neighbor_index[1]
                z_index = neighbor_index[2]

                if np.abs(mean_value_cluster - image[x_index, y_index, z_index]) < tol:
                    segmentation[x_index, y_index, z_index] = 1
                else:
                    segmentation[x_index, y_index, z_index] = 0
            
            radious = radious + 1
        call_methods_seg.mri_image = segmentation

        
    def kmeans(image, value_k, value_iter, call_methods_seg):

        values_k = np.linspace(np.amin(image), np.amax(image), value_k)

        for i in range(value_iter):
            distance = [np.abs(k-image) for k in values_k]

            kmeans_img = np.argmin(distance, axis=0)

            for k_i in range(value_k):        
                values_k[k_i] = np.mean(image[kmeans_img == k_i])
                
        call_methods_seg.mri_image = kmeans_img

    def gmm (image, call_methods_seg):
        # Each component has a weight (wi), a mean (mui), and a standard deviation (sdi)
        w1 = 1/3
        w2 = 1/3
        w3 = 1/3
        mu1 = 0
        sd1 = 50
        mu2 = 100
        sd2 = 50
        mu3 = 150
        sd3 = 50

        gmm_seg = np.zeros_like(image)
        for iter in range(1, 5) :

            # Compute likelihood of belonging to a cluster
            p1 = 1/np.sqrt(2*np.pi*sd1**2) * np.exp(-0.5*np.power(image - mu1, 2) / sd1**2)
            p2 = 1/np.sqrt(2*np.pi*sd2**2) * np.exp(-0.5*np.power(image - mu2, 2) / sd2**2)
            p3 = 1/np.sqrt(2*np.pi*sd3**2) * np.exp(-0.5*np.power(image - mu3, 2) / sd3**2)

            # Normalise probability
            r1 = np.divide(w1 * p1, w1 * p1 + w2 * p2 + w3 * p3)
            r2 = np.divide(w2 * p2, w1 * p1 + w2 * p2 + w3 * p3) 
            r3 = np.divide(w3 * p3, w1 * p1 + w2 * p2 + w3 * p3) 

            # Update parameters
            w1 = r1.mean()
            w2 = r2.mean()
            w3 = r3.mean()
            mu1 = np.multiply(r1, image).sum() / r1.sum()
            sd1 = np.sqrt(np.multiply(r1, np.power(image - mu1, 2)).sum() / r1.sum())
            mu2 = np.multiply(r2, image).sum() / r2.sum()
            sd2 = np.sqrt(np.multiply(r2, np.power(image - mu2, 2)).sum() / r2.sum())
            mu3 = np.multiply(r3, image).sum() / r3.sum()
            sd3 = np.sqrt(np.multiply(r3, np.power(image - mu3, 2)).sum() / r3.sum())

        # Perform segmentation
        gmm_seg[np.multiply(r1 > r2, r1 > r3)] = 0
        gmm_seg[np.multiply(r2 > r1, r2 > r3)] = 1
        gmm_seg[np.multiply(r3 > r1, r3 > r2)] = 2

        call_methods_seg.mri_image =  gmm_seg

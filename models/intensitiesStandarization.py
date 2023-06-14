import numpy as np
from scipy.signal import find_peaks
import scipy.stats as stats

class IntensitiesStandarization:

    def rescaling(image,call_methods_seg):
        min_value = image.min()
        max_value = image.max()

        image_data_rescaled = (image - min_value) / (max_value - min_value)
        call_methods_seg.mri_image = image_data_rescaled

    def zscore(image, call_methods_seg):
        mean = image[image > 10].mean()
        standard_deviation = image[image > 10].std()
        image_zscore = (image - mean)/(standard_deviation) 
        call_methods_seg.mri_image = image_zscore

    def white_stripe(X, call_methods_seg):
        # Calcula el histograma
        hist, bins = np.histogram(X.ravel(), bins="auto")

        # Encuentra los picos del histograma
        peaks, _ = find_peaks(hist)

        # Si hay al menos tres picos, utiliza el valor moda entre el segundo y el tercer pico como divisor
        if len(peaks) >= 3:
            last_peak = peaks[-1]
            #second_last_peak = peaks[-2]
            start_index = max(0, last_peak - 10)
            last_peak_range = range(int(bins[start_index]), int(bins[-1]) + 1)
            #second_last_peak_range = range(int(bins[second_last_peak]), int(bins[last_peak])+1)
            mode, _ = stats.mode(hist[last_peak_range])
            divisor = mode[0]
        # Si hay menos de tres picos, utiliza el valor moda de todo el histograma como divisor
        else:
            mode, _ = stats.mode(hist)
            divisor = mode[0]

        # Divide el histograma por el valor divisor
        #hist_norm = hist / divisor
        image_ws = X / divisor

        call_methods_seg.mri_image = image_ws
    
    def hist_match(source, template, call_methods_seg):
        """
        Adjust the pixel values of a grayscale image such that its histogram
        matches that of a target image

        Arguments:
        -----------
            source: np.ndarray
                Image to transform; the histogram is computed over the flattened
                array
            template: np.ndarray
                Template image; can have different dimensions to source
        Returns:
        -----------
            matched: np.ndarray
                The transformed output image
        """

        oldshape = source.shape
        source = source.ravel()
        template = template.ravel()

        # get the set of unique pixel values and their corresponding indices and
        # counts
        s_values, bin_idx, s_counts = np.unique(source, return_inverse=True,
                                                return_counts=True)
        t_values, t_counts = np.unique(template, return_counts=True)

        # take the cumsum of the counts and normalize by the number of pixels to
        # get the empirical cumulative distribution functions for the source and
        # template images (maps pixel value --> quantile)
        s_quantiles = np.cumsum(s_counts).astype(np.float64)
        s_quantiles /= s_quantiles[-1]
        t_quantiles = np.cumsum(t_counts).astype(np.float64)
        t_quantiles /= t_quantiles[-1]

        # interpolate linearly to find the pixel values in the template image
        # that correspond most closely to the quantiles in the source image
        interp_t_values = np.interp(s_quantiles, t_quantiles, t_values)

        call_methods_seg.mri_image = interp_t_values[bin_idx].reshape(oldshape)

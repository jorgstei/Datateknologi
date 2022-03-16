import numpy as np
import skimage
import utils
import pathlib
import matplotlib.pyplot as plt
import functools as ft

'''
[1.0 points] Implement a function in task2a.py/task2a.ipynb that implements Otsu’s algorithm for thresholding, and returns a single threshold value.
Segment the images thumbprint.png and polymercell.png, and include the results in your report.
'''
def sum_to_threshhold(arr: np.ndarray, threshold: int):
    sum = 0
    for i, el in enumerate(arr):
        if(i < threshold):
            sum+=el

    return sum

def mean_to_threshhold(arr: np.ndarray, threshold: int, less_than: bool):
    numerator_sum = 0
    divisor_sum = 0

    if(less_than):
        for i, el in enumerate(arr):
            if(i < threshold):
                numerator_sum += i * el
                divisor_sum += el
    else:
        for i, el in enumerate(arr):
            if(i >= threshold):
                numerator_sum += i * el
                divisor_sum += el

    return numerator_sum/divisor_sum

def otsu_thresholding(im: np.ndarray) -> int:
    """
        Otsu's thresholding algorithm that segments an image into 1 or 0 (True or False)
        The function takes in a grayscale image and outputs a boolean image

        args:
            im: np.ndarray of shape (H, W) in the range [0, 255] (dtype=np.uint8)
        return:
            (int) the computed thresholding value
    """
    assert im.dtype == np.uint8
    # START YOUR CODE HERE ### (You can change anything inside this block)
    # You can also define other helper functions

    # Compute normalized histogram
    intensity_count = np.zeros(256)
    for i in range(len(im)):
        for j in range(len(im[i])):
            intensity_count[im[i][j]] += 1

    #test = [9,6,4,5,8,4]
    num_pixels = im.shape[0]*im.shape[1]
    best_between_class_variance = -100
    best_threshold = -1
    # Check for each threshold if it produces a better between class variance
    for threshold in range(1,256):
        background_percentage = sum_to_threshhold(intensity_count, threshold)/num_pixels
        foreground_percentage = 1-background_percentage

        background_mean = mean_to_threshhold(intensity_count, threshold, True)
        foreground_mean = mean_to_threshhold(intensity_count, threshold, False)

        between_class_variance = background_percentage*foreground_percentage*(background_mean-foreground_mean)**2
        if(best_between_class_variance < between_class_variance):
            best_between_class_variance = between_class_variance
            best_threshold = threshold
    
    threshold = best_threshold
    '''
    plt.imshow(im, cmap="gray")
    plt.show()
    '''
    # Plot intensity distribution
    intensity_levels = list(range(0,256))
    plt.bar(intensity_levels, intensity_count)
    plt.show()
    
    return threshold
    ### END YOUR CODE HERE ###


if __name__ == "__main__":
    # DO NOT CHANGE
    impaths_to_segment = [
        pathlib.Path("thumbprint.png"),
        pathlib.Path("polymercell.png"),
        pathlib.Path("defective-weld.png")
    ]
    for impath in impaths_to_segment:
        im = utils.read_image(impath)
        threshold = otsu_thresholding(im)
        print("Found optimal threshold:", threshold)

        # Segment the image by threshold
        segmented_image = (im >= threshold)
        assert im.shape == segmented_image.shape, "Expected image shape ({}) to be same as thresholded image shape ({})".format(
            im.shape, segmented_image.shape)
        assert segmented_image.dtype == np.bool, "Expected thresholded image dtype to be np.bool. Was: {}".format(
            segmented_image.dtype)

        segmented_image = utils.to_uint8(segmented_image)

        save_path = "{}-segmented.png".format(impath.stem)
        utils.save_im(save_path, segmented_image)

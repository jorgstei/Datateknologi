import skimage
import skimage.io
import skimage.transform
import os
import numpy as np
import utils
import matplotlib.pyplot as plt
'''
Use what you’ve learned from the lectures and the recommended resources to remove thenoise in the image seen in Figure 5a.  Note that the noise is a periodic signal.
Also, the result youshould expect can be seen in Figure 5bInclude the filtered result in your report.Implement this in the filetask4c.py/task4c.ipynb.
Hint:Try to inspect the image in the frequency domain and see if you see any abnormal spikes that might be the noise.
'''

if __name__ == "__main__":
    # DO NOT CHANGE
    impath = os.path.join("images", "noisy_moon.png")
    im = utils.read_im(impath)
    # START YOUR CODE HERE ### (You can change anything inside this block)
    '''
    plt.figure(figsize=(20, 4))
    for i in range(10):
        plt.subplot(2, 5, i)
        kernel = utils.create_low_pass_frequency_kernel(im, 9.4+(0.05*i))
        im_filtered = np.log(np.abs(np.fft.ifft2(np.multiply(np.fft.fft2(im), np.fft.fft2(kernel)))) + 1)
        plt.imshow(im_filtered, cmap="gray")
    plt.show()
    '''
    

    plt.figure(figsize=(20, 4))
    plt.subplot(1, 5, 1)
    plt.imshow(im, cmap="gray")

    plt.subplot(1, 5, 2)
    plt.imshow(np.log(np.abs(np.fft.fftshift(np.fft.fft2(im))) + 1), cmap="gray")

    kernel = np.ones_like(im, dtype=np.float32)
    filter_rect_height = 11
    filter_rect_width_to_subtract = 25
    # Left rectangle
    kernel[im.shape[0]//2 - filter_rect_height//2 : im.shape[0]//2 + filter_rect_height//2, 0 : im.shape[1]//2 - filter_rect_width_to_subtract] = 0
    # Right rectangle
    kernel[im.shape[0]//2 - filter_rect_height//2 : im.shape[0]//2 + filter_rect_height//2, im.shape[1]//2 + filter_rect_width_to_subtract : im.shape[1]] = 0
    plt.subplot(1, 5, 3)
    plt.imshow(kernel, cmap="gray")

    fft_img_filtered = np.log(np.abs(np.fft.fftshift(np.multiply(np.fft.fft2(im), np.fft.ifftshift(kernel)))) + 1)
    plt.subplot(1,5,4)
    plt.imshow(fft_img_filtered, cmap="gray")

    spatial_result = np.log(np.abs(np.fft.ifft2(np.multiply(np.fft.fft2(im), np.fft.ifftshift(kernel)))) + 1)
    plt.subplot(1,5,5)
    plt.imshow(spatial_result, cmap="gray")

    plt.show()
    
    ### END YOUR CODE HERE ###
    utils.save_im("moon_filtered.png", utils.normalize(spatial_result))

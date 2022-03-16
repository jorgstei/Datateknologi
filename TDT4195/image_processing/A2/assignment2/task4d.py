import skimage
import skimage.io
import skimage.transform
import pathlib
import numpy as np
import utils
import matplotlib.pyplot as plt
image_dir = pathlib.Path("images")
impaths = [
    image_dir.joinpath("page1.png"),
    image_dir.joinpath("page2.png"),
    image_dir.joinpath("page4.png"),
    image_dir.joinpath("page6.png"),
    image_dir.joinpath("page7.png"),
    image_dir.joinpath("page8.png"),
]


def create_binary_image(im):
    """Creates a binary image from a greyscale image "im"

    Args:
        im ([np.ndarray, np.float]): [An image of shape [H, W] in the range [0, 1]]

    Returns:
        [np.ndarray, np.bool]: [A binary image]
    """

    # START YOUR CODE HERE ### (You can change anything inside this block)
    binary_im = np.zeros(im.shape, dtype=np.bool)
    fft_im = np.log(np.abs(np.fft.fftshift(np.fft.fft2(im))) + 1)
    
    min_val = np.amin(fft_im)
    max_val = np.amax(fft_im)
    print("Min:", min_val, "Max:", max_val)

    for i in range(len(fft_im[0])):
        for j in range(len(fft_im)):
            if(fft_im[i][j] > 6):
                binary_im[i][j] = 1

    '''
    plt.figure(figsize=(20, 4))

    plt.subplot(1, 2, 1)
    plt.imshow(fft_im, cmap="gray")
    
    plt.subplot(1, 2, 2)
    plt.imshow(binary_im, cmap="gray")
    plt.show()
    '''  

    ### END YOUR CODE HERE ###
    return binary_im


if __name__ == "__main__":
    # NO NEED TO EDIT THE CODE BELOW.
    verbose = True
    plt.figure(figsize=(4, 12))
    plt.tight_layout()
    images_to_visualize = []
    for i, impath in enumerate(impaths):
        im = utils.read_im(str(impath))
        im_binary = create_binary_image(im)
        assert im_binary.dtype == np.bool,            f"Expected the image to be of dtype np.bool, got {im_binary.dtype}"
        angles, distances = utils.find_angle(im_binary)
        angle = 0
        if len(angles) > 0:
            angle = angles[0] * 180 / np.pi
        print(f"Found angle: {angle:.2f}")
        hough_im = utils.create_hough_line_image(im, angles, distances)
        rotated = skimage.transform.rotate(im, angle, cval=im.max())
        images_to_visualize.extend([im, im_binary, hough_im, rotated])
    image = utils.np_make_image_grid(images_to_visualize, nrow=len(impaths))
    utils.save_im("task4d.png", image)
    plt.imshow(image, cmap="gray")
    plt.show()

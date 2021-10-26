import matplotlib.pyplot as plt
import pathlib
import numpy as np
from utils import read_im, save_im
output_dir = pathlib.Path("image_solutions")
output_dir.mkdir(exist_ok=True)


im = read_im(pathlib.Path("images", "lake.jpg"))
plt.imshow(im)


def greyscale(im):
    """ Converts an RGB image to greyscale

    Args:
        im ([type]): [np.array of shape [H, W, 3]]

    Returns:
        im ([type]): [np.array of shape [H, W]]
    """
    im = np.dot(im[...,:3], [0.212, 0.7152, 0.0722])

    return im


im_greyscale = greyscale(im)
save_im(output_dir.joinpath("lake_greyscale.jpg"), im_greyscale, cmap="gray")
plt.imshow(im_greyscale, cmap="gray")
plt.show()

def inverse(im):
    """ Finds the inverse of the greyscale image

    Args:
        im ([type]): [np.array of shape [H, W]]

    Returns:
        im ([type]): [np.array of shape [H, W]]
    """
    # YOUR CODE HERE
    print(im.min, im.max)
    for x in range(im.shape[0]):
        for y in range(im.shape[1]):
            im[x][y] = [1-im[x][y][0], 1-im[x][y][1], 1-im[x][y][2]]

    return im


im_inverse = inverse(im)
save_im(output_dir.joinpath("lake_inverse.jpg"), im_inverse, cmap="gray")
plt.imshow(im_inverse, cmap="gray")
plt.show()


import matplotlib.pyplot as plt
import pathlib
import numpy as np
from utils import read_im, save_im, normalize
output_dir = pathlib.Path("image_solutions")
output_dir.mkdir(exist_ok=True)


im = read_im(pathlib.Path("images", "lake.jpg"))
plt.imshow(im)


def convolve_im(im, kernel):
    """ A function that convolves im with kernel

    Args:
        im ([type]): [np.array of shape [H, W, 3]]
        kernel ([type]): [np.array of shape [K, K]]

    Returns:
        [type]: [np.array of shape [H, W, 3]. should be same as im]
    """

    
    #print(temp)
    assert len(im.shape) == 3
    # Assume odd shaped kernel
    kernel_x_offset = int((kernel.shape[0]-1)/2)
    kernel_y_offset = int((kernel.shape[1]-1)/2)

    rgb_arrays = []
    for channel in range(3):
        temp = np.zeros((im.shape[0], im.shape[1]), dtype=float)
        for x in range(im.shape[0]):
            for y in range(im.shape[1]):
                sum = 0

                for k in range(kernel.shape[0]):
                    # If kernel x-coord is outside (in padding) continue
                    if(x-kernel_x_offset+k < 0 or x-kernel_x_offset+k > im.shape[0]-1):
                        #print("Outside x")
                        continue
                    for j in range(kernel.shape[1]):
                        # If kernel y-coord is outside (in padding area) continue
                        if(y-kernel_y_offset+j < 0 or y-kernel_y_offset+j > im.shape[1]-1):
                            #print("Outside y")
                            continue

                        #print(f"Applying kernel ({k}, {j}) to im ({x}, {y})")
                        sum += kernel[k][j] * im[int(x-kernel_x_offset+k)][int(y-kernel_y_offset+j)][channel]
                        
                temp[x][y] = sum
        rgb_arrays.append(temp)

    result = np.dstack((rgb_arrays[0], rgb_arrays[1], rgb_arrays[2]))
    return result


if __name__ == "__main__":
    # Define the convolutional kernels
    h_b = 1 / 256 * np.array([
        [1, 4, 6, 4, 1],
        [4, 16, 24, 16, 4],
        [6, 24, 36, 24, 6],
        [4, 16, 24, 16, 4],
        [1, 4, 6, 4, 1]
    ])
    sobel_x = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])

    # Convolve images
    im_smoothed = convolve_im(im.copy(), h_b)
    save_im(output_dir.joinpath("im_smoothed.jpg"), im_smoothed)

    im_sobel = convolve_im(im, sobel_x)
    save_im(output_dir.joinpath("im_sobel.jpg"), im_sobel)

    # DO NOT CHANGE. Checking that your function returns as expected
    assert isinstance(
        im_smoothed, np.ndarray),         f"Your convolve function has to return a np.array. " + f"Was: {type(im_smoothed)}"
    assert im_smoothed.shape == im.shape,         f"Expected smoothed im ({im_smoothed.shape}" + \
        f"to have same shape as im ({im.shape})"
    assert im_sobel.shape == im.shape,         f"Expected smoothed im ({im_sobel.shape}" + \
        f"to have same shape as im ({im.shape})"
    plt.subplot(1, 2, 1)
    plt.imshow(normalize(im_smoothed))

    plt.subplot(1, 2, 2)
    plt.imshow(normalize(im_sobel))
    plt.show()

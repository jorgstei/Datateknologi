

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define STB_IMAGE_IMPLEMENTATION
#include "stb/stb_image.h"

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb/stb_image_write.h"

#include <windows.h>
//#include <magick_wand.h>

typedef struct{
    unsigned char r;
    unsigned char g;
    unsigned char b;
    unsigned char a;
} pixel;

int main(int argc, char** argv)
{
    stbi_set_flip_vertically_on_load(true);
	stbi_flip_vertically_on_write(true);

	int width;
	int height;
	int channels;
    unsigned char* char_pixels_1 = stbi_load(argv[1], &width, &height, &channels, STBI_rgb_alpha);
    unsigned char* char_pixels_2 = stbi_load(argv[2], &width, &height, &channels, STBI_rgb_alpha);

    printf("height:%d, width: %d\n", height, width);
    if (char_pixels_1 == NULL || char_pixels_2 == NULL)
    {
        printf("Could not load at least 1 of the 2 images, exiting.");
        exit(1);
    }
    
    //TODO 2 - typecast pointer
    pixel* pixels_1 = (pixel* ) char_pixels_1;
    pixel* pixels_2 = (pixel* ) char_pixels_2;

    //TODO 3 - malloc
    pixel* pixels_out = (pixel*)malloc(sizeof(pixel)*width*height);

    //TODO 4 - loop
    int i,j;
    for (i = 0; i < height*width; i++){ 
        pixels_out[i].r = (pixels_1[i].r + pixels_2[i].r)/2;
        pixels_out[i].g = (pixels_1[i].g + pixels_2[i].g)/2;
        pixels_out[i].b = (pixels_1[i].b + pixels_2[i].b)/2;
        pixels_out[i].a = 255;
    }

    stbi_write_png("output.png", width, height, STBI_rgb_alpha, pixels_out, sizeof(pixel) * width);

    //TODO 5 - free
    free(pixels_out);
    free(pixels_1);
    free(pixels_2);
    printf("Ending");
    return 0;
}

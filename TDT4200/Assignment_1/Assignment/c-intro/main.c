

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
// unsigned char a;
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
        printf("if was true");
        exit(1);
    }
    
    //TODO 2 - typecast pointer
    pixel* pixels_1 = (pixel* ) char_pixels_1;
    pixel* pixels_2 = (pixel* ) char_pixels_2;

    //TODO 3 - malloc
    pixel* pixels_out = (pixel*)malloc(sizeof(pixel)*width*height);

    //TODO 4 - loop
    printf("%c\n", char_pixels_1);
    int i;
    for (i = 0; i < sizeof(char_pixels_1); i++){ 
        //printf("%d",i);
    }

    stbi_write_png("output.png", width, height, STBI_rgb_alpha, char_pixels_1, sizeof(pixel) * width);

    //TODO 5 - free
    free(pixels_out);
    printf("Ending");
    return 0;
}

// Compile with: make main (nvcc main_solution.cu -o main for win)
// Run with ./main input.jpg 2 5 (or any other positive ints)
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <signal.h>

#define STB_IMAGE_IMPLEMENTATION
#include "stb/stb_image.h"

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb/stb_image_write.h"

typedef struct pixel_struct {
	unsigned char r;
	unsigned char g;
	unsigned char b;
	unsigned char a;
} pixel;

#define cudaErrCheck(ans) { gpuAssert((ans), __FILE__, __LINE__); }
inline void gpuAssert(cudaError_t code, const char *file, int line, bool abort=true) {
	if (code != cudaSuccess) {
		fprintf(stderr,"GPUassert: %s %s %d\n", cudaGetErrorString(code), file, line);
		if (abort) exit(code);
	}
}

//--------------------------------------------------------------------------------------------------
//--------------------------bilinear interpolation--------------------------------------------------
//--------------------------------------------------------------------------------------------------
// TODO 2 b: Change to device function
__device__ void bilinear(pixel* Im, float row, float col, pixel* pix, int width, int height) {

    int cm, cn, fm, fn;
    double alpha, beta;

    cm = (int)ceil(row);
    fm = (int)floor(row);
    cn = (int)ceil(col);
    fn = (int)floor(col);
    alpha = ceil(row) - row;
    beta = ceil(col) - col;

    pix->r = (unsigned char)(alpha * beta * Im[fm * width + fn].r
    	+ (1 - alpha) * beta * Im[cm * width + fn].r
        + alpha * (1 - beta) * Im[fm * width + cn].r
        + (1 - alpha) * (1 - beta) * Im[cm * width + cn].r);
    pix->g = (unsigned char)(alpha * beta * Im[fm * width + fn].g
        + (1 - alpha) * beta * Im[cm * width + fn].g
        + alpha * (1 - beta) * Im[fm * width + cn].g
        + (1 - alpha) * (1 - beta) * Im[cm * width + cn].g);
    pix->b = (unsigned char)(alpha * beta * Im[fm * width + fn].b
        + (1 - alpha) * beta * Im[cm * width + fn].b
        + alpha * (1 - beta) * Im[fm * width + cn].b
        + (1 - alpha) * (1 - beta) * Im[cm * width + cn].b);
    pix->a = 255;
}
//---------------------------------------------------------------------------
// TODO 2 a: Change to kernel
__global__ void bilinear_kernel(pixel* d_pixels_in, pixel* d_pixels_out, int in_width, int in_height, int out_width, int out_height) {
	// TODO 2 c - Parallelize the kernel
	
	//printf("Blockx %d, blockdimx %d, threadidx %d\n", blockIdx.x, blockDim.x, threadIdx.x);
	// 				Which block in grid	| 	Size of each block	| 	Which thread in block
    int x_element = 	blockIdx.x 		* 		blockDim.x 		+ 	threadIdx.x;
    int y_element = 	blockIdx.y 		* 		blockDim.y 		+ 	threadIdx.y;


    float x_in = x_element * (in_width - 1) / out_width;
    float y_in = y_element * (in_height - 1) / out_height;
	
	// Allocate jobs accordingly
    if (x_element < out_width && y_element < out_height) {
        pixel new_pixel;
        bilinear(d_pixels_in, y_in, x_in, &new_pixel, in_width, in_height);
        d_pixels_out[y_element * out_width + x_element] = new_pixel;
    }
	
}

int main(int argc, char** argv) {

	stbi_set_flip_vertically_on_load(true);
	stbi_flip_vertically_on_write(true);

	int in_width;
	int in_height;

	pixel* h_pixels_in;
	int channels;
	h_pixels_in = (pixel *) stbi_load(argv[1], &in_width, &in_height, &channels, STBI_rgb_alpha);
	if (h_pixels_in == NULL) {
		exit(1);
	}
	printf("Image dimensions: %dx%d\n", in_width, in_height);

	double scale_x = argc > 2 ? atof(argv[2]): 2;
	double scale_y = argc > 3 ? atof(argv[3]): 8;

	int out_width = in_width * scale_x;
	int out_height = in_height * scale_y;

	pixel* h_pixels_out = (pixel*) malloc(sizeof(pixel)*out_width*out_height);
	
	pixel* d_pixels_in;
	pixel* d_pixels_out;

	//TODO 1 a - cuda malloc

	//printf("Cuda malloc\n");
	cudaMalloc(&d_pixels_in, in_width*in_height*sizeof(pixel)); 
	cudaMalloc(&d_pixels_out, out_width*out_height*sizeof(pixel));

	//TODO END

   	cudaEvent_t start_transfer, stop_transfer;
	cudaEventCreate(&start_transfer);
	cudaEventCreate(&stop_transfer);
	cudaEventRecord(start_transfer);

	//TODO 1 b - cuda memcpy

	//printf("Cuda memcpy\n");
	cudaMemcpy(d_pixels_in, h_pixels_in, in_width*in_height*sizeof(pixel), cudaMemcpyHostToDevice);

	//TODO END

	// TODO 1 c - block size and grid size. gridSize should depend on the blockSize and output dimensions.
	int blocksz = 32;
	dim3 blockSize(blocksz, blocksz);
	dim3 gridSize(ceil(out_width / blocksz), ceil(out_height / blocksz));
	printf("Block dimensions: %dx%d\nGrid dimensions: %dx%d\n", blockSize.x, blockSize.y, gridSize.x, gridSize.y);

	// TODO END

   	cudaEvent_t start, stop;
	cudaEventCreate(&start);
	cudaEventCreate(&stop);
	cudaEventRecord(start);

	//TODO 2 a - GPU computation

	// Change the function call so that it becomes a kernel call. Change the input and output pixel variables to be device-side instead of host-side.
    bilinear_kernel<<<gridSize, blockSize>>>(d_pixels_in, d_pixels_out, in_width, in_height, out_width, out_height);

	// TODO END

	cudaEventRecord(stop);
	cudaDeviceSynchronize();
	//printf("Pre err\n");
	cudaError_t err = cudaGetLastError();
	if (err != cudaSuccess)
		printf("%s\n", cudaGetErrorString(err));
	cudaDeviceSynchronize();
	cudaEventSynchronize(stop);
	//printf("Post err\n");
	float spentTime = 0.0;
	cudaEventElapsedTime(&spentTime, start, stop);
	printf("Time spent %.3f seconds\n", spentTime/1000);

	//TODO 3 a - Copy the device-side data into the host-side variable
	cudaMemcpy(h_pixels_out, d_pixels_out, out_width*out_height*sizeof(pixel), cudaMemcpyDeviceToHost);
	// TODO END

	cudaEventRecord(stop_transfer);
	cudaEventSynchronize(stop_transfer);
	float spentTimeTransfer = 0.0;
	cudaEventElapsedTime(&spentTimeTransfer, start_transfer, stop_transfer);
	printf("Time spent including transfer: %.3f seconds\n", spentTimeTransfer/1000);

	// Writes the host-side data to the output file.
	stbi_write_png("output.png", out_width, out_height, STBI_rgb_alpha, h_pixels_out, sizeof(pixel) * out_width);
	
	//TODO 3 b - Free heap-allocated memory on device and host
	
	// Free host
	free(h_pixels_in);
	free(h_pixels_out);

	// Free device
	cudaFree(d_pixels_in);
	cudaFree(d_pixels_out);

	// TODO END

	return 0;
}

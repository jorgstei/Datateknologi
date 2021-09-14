


#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <signal.h>
#include "mpi.h"


#include <time.h>
#include <stdlib.h>


 

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


// Bilinear interpolation
// height is unused here..?
void bilinear(pixel* Im, float row, float col, pixel* pix, int width, int height)
{
	//printf("Start of bilin: %d\n", r);
	int cm, cn, fm, fn;
	double alpha, beta;

	cm = (int)ceil(row);
	fm = (int)floor(row);
	cn = (int)ceil(col);
	fn = (int)floor(col);
	alpha = ceil(row) - row;
	beta = ceil(col) - col;

	pix->r = (unsigned char)(alpha*beta*Im[fm*width+fn].r
			+ (1-alpha)*beta*Im[cm*width+fn].r
			+ alpha*(1-beta)*Im[fm*width+cn].r
			+ (1-alpha)*(1-beta)*Im[cm*width+cn].r );
	pix->g = (unsigned char)(alpha*beta*Im[fm*width+fn].g
			+ (1-alpha)*beta*Im[cm*width+fn].g
			+ alpha*(1-beta)*Im[fm*width+cn].g
			+ (1-alpha)*(1-beta)*Im[cm*width+cn].g );
	pix->b = (unsigned char)(alpha*beta*Im[fm*width+fn].b
			+ (1-alpha)*beta*Im[cm*width+fn].b
			+ alpha*(1-beta)*Im[fm*width+cn].b
			+ (1-alpha)*(1-beta)*Im[cm*width+cn].b );
	pix->a = 255;
	//printf("End of bilin: %d\n", r);
}
//---------------------------------------------------------------------------

//Helper function to locate the source of errors
void
SEGVFunction( int sig_num)
{
	printf ("\n		Signal %d received\n\n",sig_num);
	exit(sig_num);
}

int main(int argc, char** argv)
{
	srand((unsigned int) time(NULL));
	signal(SIGSEGV, SEGVFunction);
	stbi_set_flip_vertically_on_load(true);
	stbi_flip_vertically_on_write(true);

	//TODO 1 - init
	MPI_Init(NULL, NULL);
    
	int comm_size;
    int rank;
	MPI_Comm_size(MPI_COMM_WORLD, &comm_size);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	printf("Hello my rank is %d\n", rank);
	//TODO END


	pixel* pixels_in;

	int in_width;
	int in_height;
	int channels;


//TODO 2 - broadcast
	if(rank == 0){
		pixels_in = (pixel *) stbi_load(argv[1], &in_width, &in_height, &channels, STBI_rgb_alpha);
		printf("Hello here is pixel size: %ld\n", sizeof(pixels_in));
		if (pixels_in == NULL) {
			exit(1);
		}
		printf("Image dimensions: %dx%d\n", in_width, in_height);

		for(int dest_rank = 1; dest_rank < comm_size; dest_rank++){
			printf("Process 0 is sending information to process %d\n", dest_rank);
			MPI_Send(&pixels_in, 4, MPI_UNSIGNED_CHAR, dest_rank, 0, MPI_COMM_WORLD);
			MPI_Send(&in_width, 1, MPI_INT, dest_rank, 0, MPI_COMM_WORLD);
			MPI_Send(&in_height, 1, MPI_INT, dest_rank, 0, MPI_COMM_WORLD);
		}
	}
	else{
		printf("Process %d is attempting to receive information from process 0\n", rank);
		MPI_Recv(&pixels_in, 4, MPI_UNSIGNED_CHAR, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
		MPI_Recv(&in_width, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
		MPI_Recv(&in_height, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
		printf("Process %d got info: width=%d, height=%d\n", rank, in_width, in_height);
	}
	
	

//TODO END


	double scale_x = argc > 2 ? atof(argv[2]): 2;
	double scale_y = argc > 3 ? atof(argv[3]): 8;

	int out_width = in_width * scale_x;
	int out_height = in_height * scale_y;
	
//TODO 3 - partitioning
	int local_width = in_width;
	int local_height = in_height/comm_size;
	printf("P%d: Local width: %d and height: %d\n", rank, local_width, local_height);

	int local_out_width = out_width;
	int local_out_height = out_height/comm_size;
	printf("P%d: Local out width: %d and height: %d\n", rank, local_out_width, local_out_height);

	pixel* local_out = (pixel *) malloc(sizeof(pixel) * local_out_width * local_out_height);
//TODO END

printf("Computing with P%d. Local width: %d, Local height: %d\n", rank, local_width, local_height);

for(int i = 0; i < sizeof(pixels_in); i++){
	printf("P%d with pixels_in rgb:(%d, %d, %d)\n", rank, pixels_in[i].r, pixels_in[i].g, pixels_in[i].b);
}
//TODO 4 - computation
	for(int i= rank*local_out_height; i < (rank+1)*local_out_height; i++) {
		printf("P%d with i:%d\n", rank, i);
		for(int j = 0; j < local_out_width; j++) {
			pixel new_pixel;
			//printf("P%d calculating rows and cols\n", rank);


			float row = i * (in_height-1) / (float)out_height;
			float col = j * (in_width-1) / (float)out_width;
			//printf("Row: %f, Col: %f\n", row, col);
			printf("PROCESS%d i: %d, j: %d\n", rank, i, j);
			bilinear(pixels_in, row, col, &new_pixel, in_width, in_height);
			printf("P%d done with bilinear for i: %d, j:%d, row: %f, col: %f. Produced RGBA: (%d, %d, %d, %d)\n", rank, i, j, row, col, new_pixel.r,  new_pixel.g,  new_pixel.b,  new_pixel.a);
			local_out[i*out_width+j] = new_pixel;	
		}
	}
//TODO END
pixel* pixels_out = NULL;
if(rank==0){
	printf("P0 is allocating memory for pixels_out, pixel has sizeof:%ld\n", sizeof(pixel));
	pixels_out = malloc(sizeof(pixel)*out_width*out_height);
}

//TODO 5 - gather
MPI_Gather(&local_out, sizeof(local_out), MPI_PACKED, pixels_out, sizeof(local_out), MPI_PACKED, 0, MPI_COMM_WORLD);

if(rank == 0){
	printf("\nASDASDAS i am rank 0 in gather\n\n");
	stbi_write_png("output.png", out_width, out_height, STBI_rgb_alpha, pixels_out, sizeof(pixel) * out_width);
}
//TODO END

//TODO 1 - init
	MPI_Finalize();
//TODO END
	return 0;
}

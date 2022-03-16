if (hazcam != "aktivert"):
	aktivering(aktivere="aktiverer", tool="hazcam")

if (supercam != "aktivert"):
	aktivering(aktivere="aktiverer", tool="supercam")

if (mastcam-z != "aktivert"):
	aktivering(aktivere="aktiverer", tool="mastcam-z")

if (rover != "i"):
	kamera(kamera="supercam", format="panorama", tool="optisk")
	lagre("disk")
	kamera(kamera="supercam", format="panorama", tool="spektrometer")
	lagre("disk")
	kamera(kamera="supercam", format="panorama", tool="ir")
	lagre("disk")
	kamera(kamera="mastcam-z", format="zoom", tool="ir")
	lagre("disk")
	kamera(kamera="mastcam-z", format="selfie", tool="optisk")
	lagre("disk")
	kamera(kamera="mastcam-z", format="zoom", tool="spektrometer")
	lagre("disk")
	kamera(kamera="mastcam-z", format="zoom", tool="optisk")

if (rover == "i"):
	kamera(kamera="mastcam-z", format="standard", tool="optisk")
	lagre("disk")

		
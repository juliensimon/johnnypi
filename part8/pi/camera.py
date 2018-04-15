from picamera import PiCamera

image = "robotImage.jpg"

def takePicture():
        cam = PiCamera()
        cam.resolution=(640,480)
        cam.capture(image)
        cam.close()
	return image

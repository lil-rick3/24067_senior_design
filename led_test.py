from picamera import PiCamera
from time import sleep

camera = PiCamera()

# Adjust camera settings if needed
# camera.resolution = (width, height)
# camera.rotation = rotation_angle

# Preview the camera for 2 seconds (optional)
camera.start_preview()
sleep(2)

# Capture a photo and save it
camera.capture('/homr/julie/Desktop/test.jpg')

# Stop the preview
camera.stop_preview()
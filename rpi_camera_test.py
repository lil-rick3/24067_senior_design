import cv2
import RPi.GPIO as GPIO

# Set up GPIO
BUTTON_PIN = 17  # GPIO pin for the button (change as needed)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Function to take a picture
def take_picture(photo_num):
    ret, frame = camera.read()
    if ret:
        cv2.imwrite('captured_image' + str(photo_num) + '.jpg', frame)
        print("Picture taken!")

# Main loop
try:
    num_photos = 0
    while True:
        # Capture frame-by-frame
        ret, frame = camera.read()

        # Display the resulting frame
        cv2.imshow('Camera Preview', frame)

        # Check if the button is pressed
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            take_picture(num_photos)
            num_photos += 1

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Release the camera and close OpenCV windows
    camera.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
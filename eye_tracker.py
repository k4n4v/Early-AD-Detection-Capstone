import cv2 as cv
import matplotlib.pyplot as plt
import math

cap = cv.VideoCapture("samples/test5.mov")

initial_x = None
initial_y = None
movement_x = []
movement_y = []
coord_count = 0  # Initialize the counter for coordinates

coordinates = []
distances = []
speeds_pixels_per_second = []  # List to store the speeds in pixels/second
speeds_degrees_per_second = []  # List to store the speeds in degrees/second

# Setup specific variables
frame_time = 1/60  # Time between frames in seconds for a 60 FPS video
fov_degrees = 65.0  # Horizontal Field of View of the camera in degrees
resolution_pixels = 1920  # Width of the ROI in pixels (2000 - 900)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    roi = frame[300:800, 900:2000]  # Crop frame to right eye only
    rows, cols, _ = roi.shape
    gray_roi = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    gray_roi = cv.GaussianBlur(gray_roi, (15, 15), 0)
    
    _, threshold = cv.threshold(gray_roi, 9, 255, cv.THRESH_BINARY_INV)
    contours, _ = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv.contourArea(x), reverse=True)
    
    for cnt in contours:
        (x, y, w, h) = cv.boundingRect(cnt)
        center_x = x + int(w/2)
        center_y = y + int(h/2)
        
        # Lines showing the center of the pupil
        cv.line(roi, (center_x, 0), (center_x, rows), (0, 255, 0), 2)
        cv.line(roi, (0, center_y), (cols, center_y), (0, 255, 0), 2)

        if initial_x is None and initial_y is None:
            initial_x, initial_y = center_x, center_y

        relative_x = center_x - initial_x
        relative_y = center_y - initial_y

        # Record every frame
        movement_x.append(relative_x)
        movement_y.append(relative_y)
        
        coordinates.append((relative_x,relative_y))
        
        # Calculate distances and speeds if there is at least one previous coordinate
        if len(movement_x) > 1:
            dx = movement_x[-1] - movement_x[-2]
            dy = movement_y[-1] - movement_y[-2]
            
            distance = math.sqrt(dx**2 + dy**2)
            distances.append(distance)
            
            # Calculate and store speed in pixels/second
            speed_pixels_per_second = distance / frame_time
            speeds_pixels_per_second.append(speed_pixels_per_second)
            
            # Convert speed from pixels/second to degrees/second
            speed_degrees_per_second = speed_pixels_per_second * (fov_degrees / resolution_pixels)
            speeds_degrees_per_second.append(speed_degrees_per_second)

        break # Process only the largest contour

    cv.imshow("Frame", roi) # Display eye being tracked
    
    frame_delay = int(1000 / 60)  # For 60 FPS delay is around 16.67 ms
    key = cv.waitKey(frame_delay)  # Frame delay so it is easier to watch video preview
    if key == 27:  # ESC to quit
        break

cap.release()
cv.destroyAllWindows()


# Print the speeds list
print("Coordinates (x,y):", coordinates[:5])
print("Speeds between coordinates (pixels/second):", speeds_pixels_per_second[:5])
print("Speeds between coordinates (degrees/second):", speeds_degrees_per_second[:5])



# Plotting after the loop is finished
plt.figure()
for i, (x, y) in enumerate(zip(movement_x, movement_y)):
    plt.scatter(x, y, c='r')
    plt.annotate(f'({x}, {relative_y})', (x, y), textcoords="offset points", xytext=(0,10), ha='center')
plt.xlabel("X Movement from Initial")
plt.ylabel("Y Movement from Initial")
plt.title("Pupil Movement from Initial Position")
plt.show()

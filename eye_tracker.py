import cv2
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture("samples/test5.mov")

initial_x = None
initial_y = None
frame_count = 0
movement_x = []
movement_y = []

while True:
    ret, frame = cap.read()
    frame_count += 1
    
    if not ret:
        break

    roi = frame[300:800, 900:2000]
    rows, cols, _ = roi.shape
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray_roi = cv2.GaussianBlur(gray_roi, (15, 15), 0)
    
    _, threshold = cv2.threshold(gray_roi, 9, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        center_x = x + int(w/2)
        center_y = y + int(h/2)

        if initial_x is None and initial_y is None:
            initial_x, initial_y = center_x, center_y

        relative_x = center_x - initial_x
        relative_y = center_y - initial_y

        # Add lines showing the center of the pupil
        cv2.line(roi, (center_x, 0), (center_x, rows), (0, 255, 0), 2)
        cv2.line(roi, (0, center_y), (cols, center_y), (0, 255, 0), 2)

        if frame_count == 1:
            movement_x.append(0)
            movement_y.append(0)
        elif frame_count % 1 == 0:
            movement_x.append(relative_x)
            movement_y.append(relative_y)
            print(f"Frame {frame_count}: ({relative_x}, {relative_y})")

        break  # Only process the largest contour

    cv2.imshow("Frame", roi)
    key = cv2.waitKey(1)  # Reduced wait time might help with lag
    if key == 27:  # ESC key
        break

cv2.destroyAllWindows()

# Plotting after the loop is finished
plt.figure()
for i, (x, y) in enumerate(zip(movement_x, movement_y)):
    plt.scatter(x, y, c='r')
    plt.annotate(f'({x}, {y})', (x, y), textcoords="offset points", xytext=(0,10), ha='center')
plt.xlabel("X Movement from Initial")
plt.ylabel("Y Movement from Initial")
plt.title("Pupil Movement from Initial Position")
plt.show()

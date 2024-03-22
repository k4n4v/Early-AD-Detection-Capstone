import cv2 as cv
import math

# Setup specific variables
FRAME_TIME = 1/60  # Time between frames in seconds for a 60 FPS video
FOV_DEGREES = 65.0  # Horizontal Field of View of the camera in degrees
RESOLUTION_PIXELS = 1920  # Width of the ROI in pixels (2000 - 900)

def process_video(video_path):
    cap = cv.VideoCapture(video_path)
    initial_x, initial_y = None, None
    coordinates = []

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

        if contours:
            cnt = contours[0]  # Process only the largest contour
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

            coordinates.append((relative_x, relative_y))

        cv.imshow("Frame", roi) # Display eye being tracked


        key = cv.waitKey(16)
        if key == 27:  # ESC to quit
            break

    cap.release()
    cv.destroyAllWindows()
    return coordinates

def calculate_speeds(coordinates):
    speeds_pixels_per_second = []
    speeds_degrees_per_second = []

    if len(coordinates) > 1:
        for i in range(1, len(coordinates)):
            dx = coordinates[i][0] - coordinates[i-1][0]
            dy = coordinates[i][1] - coordinates[i-1][1]
            distance = math.sqrt(dx**2 + dy**2)

            speed_pixels_per_second = distance / FRAME_TIME
            speeds_pixels_per_second.append(speed_pixels_per_second)

            speed_degrees_per_second = speed_pixels_per_second * (FOV_DEGREES / RESOLUTION_PIXELS)
            speeds_degrees_per_second.append(speed_degrees_per_second)

    return speeds_pixels_per_second, speeds_degrees_per_second

def main():
    video_path = "samples/test5.mov"
    coordinates = process_video(video_path)
    speeds_pixels_per_second, speeds_degrees_per_second = calculate_speeds(coordinates)

    # Results (for example purposes, displaying first few values)
    print("Speeds in pixels/second:", speeds_pixels_per_second[:5])
    print("Speeds in degrees/second:", speeds_degrees_per_second[:5])

if __name__ == "__main__":
    main()

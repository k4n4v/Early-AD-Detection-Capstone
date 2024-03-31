import cv2 as cv
import matplotlib.pyplot as plt


def initialize_video_capture(video_path):
    """Initializes and returns a video capture object for the given video file."""
    return cv.VideoCapture(video_path)


def process_frame(frame, eye_roi, initial_x, initial_y, save_threshold_image=False, save_tracking_image=False):
    """Processes a single frame to find and mark the center of the largest contour, typically the pupil, within a specified region of interest (ROI)."""
    roi = frame[eye_roi]
    rows, cols, _ = roi.shape
    gray_roi = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    gray_roi = cv.GaussianBlur(gray_roi, (15, 15), 0)
    _, threshold = cv.threshold(gray_roi, 9, 255, cv.THRESH_BINARY_INV)
    contours, _ = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv.contourArea(x), reverse=True)

    if contours:
        cnt = contours[0]  # Process only the largest contour
        (x, y, w, h) = cv.boundingRect(cnt)
        center_x = x + int(w / 2)
        center_y = y + int(h / 2)
        
        # Save the image with the threshold if not saved already
        if save_threshold_image:
            threshold_image_path = "report_template/threshold.png"
            cv.imwrite(threshold_image_path, threshold)
            save_threshold_image = False  # Reset flag to prevent further saves

        # Lines to show the center of the pupil
        cv.line(roi, (center_x, 0), (center_x, rows), (0, 255, 0), 2)
        cv.line(roi, (0, center_y), (cols, center_y), (0, 255, 0), 2)

        # Save the image with tracking lines if not saved already
        if save_tracking_image:
            tracking_image_path = "report_template/tracking.png"
            cv.imwrite(tracking_image_path, roi)
            save_tracking_image = False  # Reset flag to prevent further saves

        if initial_x is None and initial_y is None:
            initial_x, initial_y = center_x, center_y

        relative_x = center_x - initial_x
        relative_y = center_y - initial_y

        return roi, (relative_x, relative_y), initial_x, initial_y, save_threshold_image, save_tracking_image
    return roi, None, initial_x, initial_y, save_threshold_image, save_tracking_image


def clean_up(cap):
    """Releases video capture and closes all OpenCV windows."""
    cap.release()
    cv.destroyAllWindows()


def process_video(video_path, eye_roi, show_tracking):
    """Processes a video to track and calculate the relative movements of the pupil within a specified ROI across frames."""
    cap = initialize_video_capture(video_path)
    initial_x, initial_y = None, None
    coordinates = []
    save_threshold_image = True  # Initial flag to save contour image once
    save_tracking_image = True  # Initial flag to save tracking image once

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        roi, relative_position, initial_x, initial_y, save_threshold_image, save_tracking_image = process_frame(frame, eye_roi, initial_x, initial_y, save_threshold_image, save_tracking_image)
        if relative_position:
            coordinates.append(relative_position)

        delay = 1
        if show_tracking:
            cv.imshow("Frame", roi)  # Display eye being tracked
            delay = 16
            
        key = cv.waitKey(delay)
        if key == 27:  # ESC to quit
            break

    clean_up(cap)
    return coordinates


def plot_coordinates(coordinates, show_plot):
    """Plots and saves the relative movements of the pupil on an XY graph."""
    if not coordinates:
        print("No coordinates to plot.")
        return
    
    x_values, y_values = zip(*coordinates)  # Unpack the list of coordinates into separate lists for X and Y

    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='red')
    plt.title("Pupil Movement Relative to Initial Position")
    plt.xlabel("Relative X Position")
    plt.ylabel("Relative Y Position")
    plt.grid(True)
    
    # Save the figure to a file
    plt.savefig("report_template/pupil_movement_plot.png", format='png', dpi=300)
    # Show the plot
    
    if show_plot:
        plt.show()

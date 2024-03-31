from datetime import date
from eye_tracker import plot_coordinates, process_video
from saccade_detection import saccade_detection
from report_generator import create_output_report

SHOW_TRACKING = False
SHOW_PLOT = False
VIDEO_PATH = "samples/sample1.mp4"

def main():
    
    # Participant data
    participant_data = {
        '{{date}}': str(date.today()),
        '{{name}}': 'John Doe',
        '{{address}}': '123 Maple Street, Suite 101, Ottawa, ON K1A 0B1',
        '{{number}}': '123-456-7890',
        '{{age}}': '30',
        '{{sex}}': 'Male',
        '{{eye}}': 'Right',
        '{{irregular}}': '50%',
        '{{regular}}': '50%',
        '{{notes}}': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Vestibulum morbi blandit cursus risus at ultrices mi. Congue nisi vitae suscipit tellus mauris a. Sit amet consectetur adipiscing elit duis tristique. Ultrices vitae auctor eu augue ut lectus arcu. Euismod quis viverra nibh cras. '
    }
    
    # Define eye regions
    right_eye = (slice(300, 800), slice(700, 1500))
    left_eye = (slice(300, 800), slice(700, 1500))

    coordinates = process_video(VIDEO_PATH, right_eye, SHOW_TRACKING)
    plot_coordinates(coordinates, SHOW_PLOT)
    good, bad = saccade_detection(coordinates)    
    create_output_report(participant_data)

    # Results
    print("Coordinates:", coordinates)
    print(len(coordinates))
    print(f"Saccade Detection:\nGood: {good}\nBad:{bad}")

if __name__ == "__main__":
    main()

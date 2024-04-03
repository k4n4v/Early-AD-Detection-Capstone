from datetime import date
from eye_tracker import plot_coordinates, process_video
from saccade_detection import saccade_detection, select_eye
from report_generator import create_output_report

SHOW_TRACKING = True 
SHOW_PLOT = True
VIDEO_PATH = "samples/sample2.mp4"

def main():
    
    eye_slice, eye_choice = select_eye() # User input for region of intrest (ROI)
    
    coordinates = process_video(VIDEO_PATH, eye_slice, SHOW_TRACKING)
    plot_coordinates(coordinates, SHOW_PLOT)
    regular, irregular = saccade_detection(coordinates)   
    irregular_percentage = irregular / (regular+irregular) * 100
    
    # Participant data
    participant_data = {
        '{{date}}': str(date.today()),
        '{{name}}': 'Tony Stark',
        '{{address}}': '10880 Malibu Point, Malibu, California 90265',
        '{{phone}}': '212-970-4133',
        '{{age}}': '38',
        '{{sex}}': 'Male',
        '{{eye}}': eye_choice,
        '{{irregular}}': f'{str(irregular_percentage)}%',
        '{{notes}}': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Vestibulum morbi blandit cursus risus at ultrices mi. Congue nisi vitae suscipit tellus mauris a. Sit amet consectetur adipiscing elit duis tristique. Ultrices vitae auctor eu augue ut lectus arcu. Euismod quis viverra nibh cras. '
    }
     
    create_output_report(participant_data)

    # Print results to terminal
    #print("Coordinates:", coordinates)
    #print(f"Saccade Detection:\tRegular: \t{regular}\tIrregular:{irregular}")

if __name__ == "__main__":
    main()

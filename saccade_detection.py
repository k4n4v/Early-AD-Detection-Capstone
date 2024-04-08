def select_eye():
    # Ask the user to select an eye, with "right" as the default
    choice = input("Please select an eye to process (left/right). Default is right: ").lower().strip()
    
    # Return the corresponding slice based on the user's input
    # Default to the right eye if the input is unrecognized
    if choice == "left":
        return (slice(300, 800), slice(400, 1100)), "Left"
    else:
        # Default to right eye
        return (slice(300, 800), slice(700, 1500)), "Right"

def saccade_detection(coordinates):
    
    regular = 0
    irregular = 0

    # Loop through the coordinates starting at 132 and checking every 282 points
    for i in range(131, len(coordinates), 282):
        change_within_7 = False

        # Check if there are at least 7 points after the current index
        if i + 9 < len(coordinates):
            # Check the next 7 points for any change
            for j in range(i+1, i+8):
                dx = abs(coordinates[i][0] - coordinates[j][0])
                dy = abs(coordinates[i][1] - coordinates[j][1])

                if dx >= 4 or dy >= 4: # Check if either x or y changes by at least 4 points
                    change_within_7 = True
                    break 

            # Update counters based on whether a change was found within 9 points
            if change_within_7:
                regular += 1
            else:
                irregular += 1

    return regular, irregular

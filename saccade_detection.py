def saccade_detection(coordinates):
    
    good = 0
    bad = 0

    # Loop through the coordinates starting at 132 and checking every 282 points
    for i in range(131, len(coordinates), 282):

        change_within_9 = False
        
        # Check if there are at least 9 points after the current index
        if i + 9 < len(coordinates):
            # Check the next 9 points for any change
            for j in range(i+1, i+10):
                if coordinates[i] != coordinates[j]:
                    change_within_9 = True
                    break  # Stop checking further if a change is found within 9 points

            # Update counters based on whether a change was found within 9 points
            if change_within_9:
                good += 1
            else:
                bad += 1

    return good, bad



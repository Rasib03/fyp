import cv2
import numpy as np
import features
import utilities
import math

# BASELINE Angle
MIN_HANDWRITING_HEIGHT_PIXEL = 20
def straighten(image):
    global BASELINE_ANGLE

    angle_sum = 0.0
    contour_count = 0

    # Convert to grayscale if the image is in color
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Apply bilateral filter
    filtered = cv2.bilateralFilter(gray, 3, 75, 75)

    # Binarize the image with inverted thresholding
    _, thresh = cv2.threshold(filtered, 120, 255, cv2.THRESH_BINARY_INV)

    # Dilate to connect handwritten lines
    kernel = np.ones((9, 180), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    # Find contours
    ctrs, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a copy of the original image to modify
    result = image.copy()

    for i, ctr in enumerate(ctrs):
        x, y, w, h = cv2.boundingRect(ctr)

        # Skip contours that are unlikely to be lines
        if h > w or h < MIN_HANDWRITING_HEIGHT_PIXEL:
            continue

        # We extract the region of interest/contour to be straightened.
        roi = image[y:y+h, x:x+w]

        # Skip short lines (less than half the image width)
        if w < image.shape[1] / 2:
            roi = 255
            image[y:y+h, x:x+w] = roi
            continue

        # Draw bounding box (red color, thickness 2)
        cv2.rectangle(result, (x, y), (x+w, y+h), (0, 0, 255), 2)

        # Get the minimum area rectangle for the contour
        rect = cv2.minAreaRect(ctr)
        angle = rect[2]

        # Adjust the angle to ensure proper orientation
        if angle < -45.0:
            angle += 90.0
        if angle > 45.0:
            angle -= 90.0

        # Skip if the angle is too large
        if abs(angle) > 30.0:
            continue

        rot = cv2.getRotationMatrix2D(((x+w)/2, (y+h)/2), angle, 1)
            
        extract = cv2.warpAffine(
            roi, rot, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
        
        image[y:y+h, x:x+w] = extract

        angle_sum += angle
        contour_count += 1

    # Calculate the mean angle
    if contour_count == 0:
        mean_angle = 0
    else:
        mean_angle = angle_sum / contour_count

    features.BASELINE_ANGLE = mean_angle

    return image


# LETTER_SIZE, LINE_SPACING, TOP_MARGIN
def extract_size_spacing_topMargin(img):
    # Apply bilateral filter
    filtered = utilities.bilateralFilter(img, 5)

    # Convert to grayscale and binarize
    thresh = utilities.threshold(filtered, 160)

    # Make a copy for visualization
    img_with_boxes = img.copy()
    if len(img_with_boxes.shape) == 2:
        img_with_boxes = cv2.cvtColor(img_with_boxes, cv2.COLOR_GRAY2BGR)

    # [Previous processing steps until after thresholding...]

    # After thresholding (thresh image is available)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around all contours
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 10 and h > 10:  # Filter out small noise
            cv2.rectangle(img_with_boxes,
                        (x, y),
                        (x+w, y+h),
                        (0, 255, 0),
                        1)

    

    # Apply morphological closing to connect disjointed parts of lines
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Horizontal projection
    hpList = utilities.horizontalProjection(thresh)

    # Extract top margin
    topMarginCount = 0
    for sum in hpList:
        if sum <= 255:
            topMarginCount += 1
        else:
            break
    features.TOP_MARGIN = topMarginCount  # Store top margin value

    # Coarse contour extraction
    lineTop = 0
    lineBottom = 0
    spaceTop = 0
    spaceBottom = 0
    indexCount = 0
    setLineTop = True
    setSpaceTop = True
    includeNextSpace = True
    space_zero = []
    lines = []

    for i, sum in enumerate(hpList):
        if sum == 0:
            if setSpaceTop:
                spaceTop = indexCount
                setSpaceTop = False
            indexCount += 1
            spaceBottom = indexCount
            if i < len(hpList) - 1:
                if hpList[i + 1] == 0:
                    continue
            if includeNextSpace:
                space_zero.append(spaceBottom - spaceTop)
            else:
                previous = 0 if len(space_zero) == 0 else space_zero.pop()
                space_zero.append(previous + spaceBottom - lineTop)
            setSpaceTop = True
        else:
            if setLineTop:
                lineTop = indexCount
                setLineTop = False
            indexCount += 1
            lineBottom = indexCount
            if i < len(hpList) - 1:
                if hpList[i + 1] > 0:
                    continue
                if lineBottom - lineTop < 20:
                    includeNextSpace = False
                    setLineTop = True
                    continue
            includeNextSpace = True
            lines.append([lineTop, lineBottom])
            setLineTop = True

    # Fine line segmentation with improved smoothing and merging
    fineLines = []
    MIN_LINE_HEIGHT = 20
    MIN_GAP = 15

    for i, line in enumerate(lines):
        anchor = line[0]
        anchorPoints = []
        upHill = True
        downHill = False
        segment = hpList[line[0]:line[1]]

        # Smooth the projection with a larger window
        smoothed_segment = np.convolve(segment, np.ones(10)/10, mode='valid')
        pad_len = len(segment) - len(smoothed_segment)
        smoothed_segment = np.pad(smoothed_segment, (pad_len//2, pad_len - pad_len//2), mode='edge')

        # Dynamically set ANCHOR_POINT based on the median projection value
        ANCHOR_POINT = np.median(smoothed_segment[smoothed_segment > 0]) * 0.5
        if ANCHOR_POINT < 500:
            ANCHOR_POINT = 500

        for j, sum in enumerate(smoothed_segment):
            if upHill:
                if sum < ANCHOR_POINT:
                    anchor += 1
                    continue
                anchorPoints.append(anchor)
                upHill = False
                downHill = True
            if downHill:
                if sum > ANCHOR_POINT:
                    anchor += 1
                    continue
                anchorPoints.append(anchor)
                downHill = False
                upHill = True

        if len(anchorPoints) < 2:
            fineLines.append([line[0], line[1]])
            continue

        # Merge close segments
        merged_anchorPoints = [anchorPoints[0]]
        for j in range(1, len(anchorPoints)):
            if anchorPoints[j] - merged_anchorPoints[-1] < MIN_GAP:
                continue
            merged_anchorPoints.append(anchorPoints[j])

        # Build fine lines, skipping empty segments
        lineTop = line[0]
        for x in range(1, len(merged_anchorPoints) - 1, 2):
            lineMid = int((merged_anchorPoints[x] + merged_anchorPoints[x + 1]) / 2)
            lineBottom = lineMid
            if lineBottom - lineTop < MIN_LINE_HEIGHT or lineBottom == lineTop:
                continue
            fineLines.append([lineTop, lineBottom])
            lineTop = lineBottom
        # Add the last segment if valid
        if line[1] - lineTop >= MIN_LINE_HEIGHT and line[1] != lineTop:
            fineLines.append([lineTop, line[1]])
        elif not fineLines or fineLines[-1] != [line[0], line[1]]:
            fineLines.append([line[0], line[1]])

    # Feature extraction
    space_nonzero_row_count = 0
    midzone_row_count = 0
    lines_having_midzone_count = 0
    flag = False
    MIDZONE_THRESHOLD = 15000

    for i, line in enumerate(fineLines):
        segment = hpList[line[0]:line[1]]
        for j, sum in enumerate(segment):
            if sum < MIDZONE_THRESHOLD:
                space_nonzero_row_count += 1
            else:
                midzone_row_count += 1
                flag = True
        if flag:
            lines_having_midzone_count += 1
            flag = False

    if lines_having_midzone_count == 0:
        lines_having_midzone_count = 1

    total_space_row_count = space_nonzero_row_count + np.sum(space_zero[1:-1])
    average_line_spacing = float(total_space_row_count) / lines_having_midzone_count
    average_letter_size = float(midzone_row_count) / lines_having_midzone_count
    features.LETTER_SIZE = average_letter_size

    if average_letter_size == 0:
        average_letter_size = 1
    relative_line_spacing = average_line_spacing / average_letter_size
    features.LINE_SPACING = relative_line_spacing

    return fineLines


# PEN PRESSURE
def barometer(image):
    # it's extremely necessary to convert to grayscale first
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # inverting the image pixel by pixel individually. This costs the maximum time and processing in the entire process!
    h, w = image.shape[:]
    inverted = image
    for x in range(h):
        for y in range(w):
            inverted[x][y] = 255 - image[x][y]    

    # bilateral filtering
    filtered = utilities.bilateralFilter(inverted, 3)

    # binary thresholding. Here we use 'threshold to zero' which is crucial for what we want.
    # If src(x,y) is lower than threshold=100, the new pixel value will be set to 0, else it will be left untouched!
    ret, thresh = cv2.threshold(filtered, 100, 255, cv2.THRESH_TOZERO)
    

    # add up all the non-zero pixel values in the image and divide by the number of them to find the average pixel value in the whole image
    total_intensity = 0
    pixel_count = 0
    for x in range(h):
        for y in range(w):
            if (thresh[x][y] > 0):
                total_intensity = np.int64(total_intensity)
                total_intensity += np.int64(thresh[x][y])
                pixel_count += 1

    average_intensity = float(total_intensity) / pixel_count
    features.PEN_PRESSURE = average_intensity
    return


# WORD SPACING
def extractWords(image, lines):
    # apply bilateral filter
    filtered = utilities.bilateralFilter(image, 5)

    # convert to grayscale and binarize the image by INVERTED binary thresholding
    thresh = utilities.threshold(filtered, 180)
    # cv2.imshow('thresh', wthresh)

    # Width of the whole document is found once.
    width = thresh.shape[1]
    space_zero = []  # stores the amount of space between words
    words = []  # a 2D list storing the coordinates of each word: y1, y2, x1, x2

    # Isolated words or components will be extacted from each line by looking at occurance of 0's in its vertical projection.
    for i, line in enumerate(lines):
        extract = thresh[line[0]:line[1], 0:width]  # y1:y2, x1:x2
        vp = utilities.verticalProjection(extract)
        # print i
        # print vp

        wordStart = 0
        wordEnd = 0
        spaceStart = 0
        spaceEnd = 0
        indexCount = 0
        setWordStart = True
        setSpaceStart = True
        includeNextSpace = True
        spaces = []

        # we are scanning the vertical projection
        for j, sum in enumerate(vp):
            # sum being 0 means blank space
            if (sum == 0):
                if (setSpaceStart):
                    spaceStart = indexCount
                    # spaceStart will be set once for each start of a space between lines
                    setSpaceStart = False
                indexCount += 1
                spaceEnd = indexCount
                if (j < len(vp)-1):  # this condition is necessary to avoid array index out of bound error
                    # if the next vertical projectin is 0, keep on counting, it's still in blank space
                    if (vp[j+1] == 0):
                        continue

                # we ignore spaces which is smaller than half the average letter size
                if ((spaceEnd-spaceStart) > int(features.LETTER_SIZE/2)):
                    spaces.append(spaceEnd-spaceStart)

                # next time we encounter 0, it's begining of another space so we set new spaceStart
                setSpaceStart = True

            # sum greater than 0 means word/component
            if (sum > 0):
                if (setWordStart):
                    wordStart = indexCount
                    setWordStart = False  # wordStart will be set once for each start of a new word/component
                indexCount += 1
                wordEnd = indexCount
                if (j < len(vp)-1):  # this condition is necessary to avoid array index out of bound error
                    # if the next horizontal projectin is > 0, keep on counting, it's still in non-space zone
                    if (vp[j+1] > 0):
                        continue

                # append the coordinates of each word/component: y1, y2, x1, x2 in 'words'
                # we ignore the ones which has height smaller than half the average letter size
                # this will remove full stops and commas as an individual component
                count = 0
                for k in range(line[1]-line[0]):
                    row = thresh[line[0]+k:line[0]+k+1,
                                 wordStart:wordEnd]  # y1:y2, x1:x2
                    if (np.sum(row)):
                        count += 1
                if (count > int(features.LETTER_SIZE/2)):
                    words.append([line[0], line[1], wordStart, wordEnd])

                # next time we encounter value > 0, it's begining of another word/component so we set new wordStart
                setWordStart = True

        space_zero.extend(spaces[1:-1])

    # print space_zero
    space_columns = np.sum(space_zero)
    space_count = len(space_zero)
    if (space_count == 0):
        space_count = 1
    average_word_spacing = float(space_columns) / space_count
    if features.LETTER_SIZE == 0:
        relative_word_spacing = 0
    else:
        relative_word_spacing = average_word_spacing / features.LETTER_SIZE
    features.WORD_SPACING = relative_word_spacing

    return words

# SLANT
def extractSlant(img, words):
    '''
	0.01 radian = 0.5729578 degree :: I had to put this instead of 0.0 becuase there was a bug yeilding inacurate value which I could not figure out!
	5 degree = 0.0872665 radian :: Hardly noticeable or a very little slant
	15 degree = 0.261799 radian :: Easily noticeable or average slant
	30 degree = 0.523599 radian :: Above average slant
	45 degree = 0.785398 radian :: Extreme slant
	'''
    # We are checking for 9 different values of angle
    theta = [-0.785398, -0.523599, -0.261799, -0.0872665,
             0.01, 0.0872665, 0.261799, 0.523599, 0.785398]
   
    # Corresponding index of the biggest value in s_function will be the index of the most likely angle in 'theta'
    s_function = [0.0] * 9
    count_ = [0]*9

    # apply bilateral filter
    filtered = utilities.bilateralFilter(img, 5)

    # convert to grayscale and binarize the image by INVERTED binary thresholding
    # it's better to clear unwanted dark areas at the document left edge and use a high threshold value to preserve more text pixels
    thresh = utilities.threshold(filtered, 180)
 

    # loop for each value of angle in theta
    for i, angle in enumerate(theta):
        s_temp = 0.0  # overall sum of the functions of all the columns of all the words!
        count = 0  # just counting the number of columns considered to contain a vertical stroke and thus contributing to s_temp

        # loop for each word
        for j, word in enumerate(words):
            original = thresh[word[0]:word[1], word[2]:word[3]]  # y1:y2, x1:x2

            height = word[1]-word[0]
            width = word[3]-word[2]

            # the distance in pixel we will shift for affine transformation
            # it's divided by 2 because the uppermost point and the lowermost points are being equally shifted in opposite directions
            shift = (math.tan(angle) * height) / 2

            # the amount of extra space we need to add to the original image to preserve information
            # yes, this is adding more number of columns but the effect of this will be negligible
            pad_length = abs(int(shift))

            # create a new image that can perfectly hold the transformed and thus widened image
            blank_image = np.zeros((height, width+pad_length*2, 3), np.uint8)
            new_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)
            new_image[:, pad_length:width+pad_length] = original

            # points to consider for affine transformation
            (height, width) = new_image.shape[:2]
            x1 = width/2
            y1 = 0
            x2 = width/4
            y2 = height
            x3 = 3*width/4
            y3 = height

            pts1 = np.float32([[x1, y1], [x2, y2], [x3, y3]])
            pts2 = np.float32([[x1+shift, y1], [x2-shift, y2], [x3-shift, y3]])
            M = cv2.getAffineTransform(pts1, pts2)
            deslanted = cv2.warpAffine(new_image, M, (width, height))

            # find the vertical projection on the transformed image
            vp = utilities.verticalProjection(deslanted)

            # loop for each value of vertical projection, which is for each column in the word image
            for k, sum in enumerate(vp):
                # the columns is empty
                if (sum == 0):
                    continue

                # this is the number of foreground pixels in the column being considered
                num_fgpixel = sum / 255

                # if number of foreground pixels is less than onethird of total pixels, it is not a vertical stroke so we can ignore
                if (num_fgpixel < int(height/3)):
                    continue

                # the column itself is extracted, and flattened for easy operation
                column = deslanted[0:height, k:k+1]
                column = column.flatten()

                # now we are going to find the distance between topmost pixel and bottom-most pixel
                # l counts the number of empty pixels from top until and upto a foreground pixel is discovered
                for l, pixel in enumerate(column):
                    if (pixel == 0):
                        continue
                    break
                # m counts the number of empty pixels from bottom until and upto a foreground pixel is discovered
                for m, pixel in enumerate(column[::-1]):
                    if (pixel == 0):
                        continue
                    break

                # the distance is found as delta_y, I just followed the naming convention in the research paper I followed
                delta_y = height - (l+m)

                # please refer the research paper for more details of this function, anyway it's nothing tricky
                h_sq = (float(num_fgpixel)/delta_y)**2

                # I am multiplying by a factor of num_fgpixel/height to the above function to yeild better result
                # this will also somewhat negate the effect of adding more columns and different column counts in the transformed image of the same word
                h_wted = (h_sq * num_fgpixel) / height

                # add up the values from all the loops of ALL the columns of ALL the words in the image
                s_temp += h_wted

                count += 1

        s_function[i] = s_temp
        count_[i] = count

    # finding the largest value and corresponding index
    max_value = 0.0
    max_index = 4
    for index, value in enumerate(s_function):
        # print str(index)+" "+str(value)+" "+str(count_[index])
        if (value > max_value):
            max_value = value
            max_index = index

    # We will add another value 9 manually to indicate irregular slant behaviour.
    # This will be seen as value 4 (no slant) but 2 corresponding angles of opposite sign will have very close values.
    if (max_index == 0):
        angle = 45
    elif (max_index == 1):
        angle = 30
    elif (max_index == 2):
        angle = 15
    elif (max_index == 3):
        angle = 5
    elif (max_index == 5):
        angle = -5
    elif (max_index == 6):
        angle = -15
    elif (max_index == 7):
        angle = -30
    elif (max_index == 8):
        angle = -45
    elif (max_index == 4):
        if s_function[3]==0:
            p=0
        else:
            p = s_function[4] / s_function[3]
        if s_function[5]==0:
            q=0
        else:
            q = s_function[4] / s_function[5]
        # the constants here are abritrary but I think suits the best
        if ((p <= 1.2 and q <= 1.2) or (p > 1.4 and q > 1.4)):
            angle = 0
        elif ((p <= 1.2 and q-p > 0.4) or (q <= 1.2 and p-q > 0.4)):
            angle = 0
        else:
            max_index = 9
            angle = 180

    features.SLANT_ANGLE = angle
    
    return
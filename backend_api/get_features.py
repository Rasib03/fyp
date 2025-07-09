import cv2
import extract
import features

def start(image):
    # read image from disk
    image = cv2.resize(image,(850,850))

    # Extract pen pressure.
    extract.barometer(image)

    # apply contour operation to straighten the contours which may be a single line or composed of multiple lines
    # the returned image is straightened version of the original image without filtration and binarization
    straightened = extract.straighten(image)

    # extract lines of handwritten text from the image using the horizontal projection
    # it returns a 2D list of the vertical starting and ending index/pixel row location of each line in the handwriting
    lineIndices = extract.extract_size_spacing_topMargin(straightened)
   
    # extract words from each line using vertical projection
    # it returns a 4D list of the vertical starting and ending indices and horizontal starting and ending indices (in that order) of each word in the handwriting
    wordCoordinates = extract.extractWords(straightened, lineIndices)

    # extract average slant angle of all the words containing a long vertical stroke
    extract.extractSlant(straightened, wordCoordinates)

    BASELINE_ANGLE = round(features.BASELINE_ANGLE, 2)
    TOP_MARGIN = round(features.TOP_MARGIN, 2)
    LETTER_SIZE = round(features.LETTER_SIZE, 2)
    LINE_SPACING = round(features.LINE_SPACING, 2)
    WORD_SPACING = round(features.WORD_SPACING, 2)
    PEN_PRESSURE = round(features.PEN_PRESSURE, 2)
    SLANT_ANGLE = round(features.SLANT_ANGLE, 2)

    return [BASELINE_ANGLE, TOP_MARGIN, LETTER_SIZE, LINE_SPACING, WORD_SPACING, PEN_PRESSURE, SLANT_ANGLE]
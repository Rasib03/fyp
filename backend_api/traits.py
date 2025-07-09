import os

def determine_trait_1(baseline_angle, slant_angle):
    # trait_1 = emotional stability | 1 = stable, 0 = not stable
    if (slant_angle == 0 or slant_angle == 4 or slant_angle == 6 or baseline_angle == 0):
        return 0
    else:
        return 1

def determine_trait_2(letter_size, pen_pressure):
    # trait_2 = mental energy or will power | 1 = high or average, 0 = low
    if ((pen_pressure == 0 or pen_pressure == 2) or (letter_size == 1 or letter_size == 2)):
        return 1
    else:
        return 0

def determine_trait_3(top_margin, letter_size):
    # trait_3 = modesty | 1 = observed, 0 = not observed (not necessarily the opposite)
    if (top_margin == 0 or letter_size == 1):
        return 1
    else:
        return 0

def determine_trait_4(line_spacing, word_spacing):
    # trait_4 = personal harmony and flexibility | 1 = harmonious, 0 = non harmonious
    if (line_spacing == 2 and word_spacing == 2):
        return 1
    else:
        return 0

def determine_trait_5(top_margin, slant_angle):
    # trait_5 = lack of discipline | 1 = observed, 0 = not observed (not necessarily the opposite)
    if (top_margin == 1 and slant_angle == 6):
        return 1
    else:
        return 0

def determine_trait_6(letter_size, line_spacing):
    # trait_6 = poor concentration power | 1 = observed, 0 = not observed (not necessarily the opposite)
    if (letter_size == 0 and line_spacing == 1):
        return 1
    else:
        return 0

def determine_trait_7(letter_size, word_spacing):
    # trait_7 = non communicativeness | 1 = observed, 0 = not observed (not necessarily the opposite)
    if (letter_size == 1 and word_spacing == 0):
        return 1
    else:
        return 0

def determine_trait_8(line_spacing, word_spacing):
    # trait_8 = social isolation | 1 = observed, 0 = not observed (not necessarily the opposite)
    if (word_spacing == 0 or line_spacing == 0):
        return 1
    else:
        return 0

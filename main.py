import pytesseract
from PIL import Image
import os
import cv2


def recognize_text(image_path):
    # Open image with Pillow
    image = Image.open(image_path)

    # Convert image to black and white
    bw_image = image.convert('L')

    # Save the black and white image
    base, ext = os.path.splitext(image_path)
    bw_image_path = f"{base}_bw{ext}"
    bw_image.save(bw_image_path)

    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(bw_image)

    return text


def match_symbol_orb(card_image_path, logo_path):
    # Load the image and the logo
    image = cv2.imread(card_image_path, 0)  # 0 for grayscale
    logo = cv2.imread(logo_path, 0)

    # Initialize the ORB detector
    orb = cv2.ORB_create(10000)

    # Find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(image, None)
    kp2, des2 = orb.detectAndCompute(logo, None)

    if des1 is not None and des2 is not None:
        # Create a BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # Match descriptors
        matches = bf.match(des1, des2)

        # Sort them in the order of their distance
        matches = sorted(matches, key=lambda x: x.distance)

        return len(matches)
    else:
        return -1


def match_symbol_sift(card_image_path, logo_path):
    # Load the image and the logo
    image = cv2.imread(card_image_path, 0)  # 0 for grayscale
    logo = cv2.imread(logo_path, 0)

    # Initialize the SIFT detector
    sift = cv2.SIFT_create()

    # Find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(image, None)
    kp2, des2 = sift.detectAndCompute(logo, None)

    if des1 is not None and des2 is not None:
        # Create a BFMatcher object
        bf = cv2.BFMatcher()

        # Match descriptors
        matches = bf.knnMatch(des1, des2, k=2)

        # Apply ratio test
        good_matches = []
        for match in matches:
            if len(match) >= 2:
                m, n = match
                if m.distance < 0.75 * n.distance:
                    good_matches.append([m])
            else:
                return -1

        return len(good_matches)
    else:
        return -2


def match_symbol_surf(card_image_path, logo_path):
    # Load the image and the logo
    image = cv2.imread(card_image_path, 0)  # 0 for grayscale
    logo = cv2.imread(logo_path, 0)

    # Initialize the SURF detector
    surf = cv2.xfeatures2d.SURF_create()

    # Find the keypoints and descriptors with SURF
    kp1, des1 = surf.detectAndCompute(image, None)
    kp2, des2 = surf.detectAndCompute(logo, None)

    if des1 is not None and des2 is not None:
        # Create a BFMatcher object
        bf = cv2.BFMatcher()

        # Match descriptors
        matches = bf.knnMatch(des1, des2, k=2)

        # Apply ratio test
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append([m])

        return len(good_matches)
    else:
        return -1


def get_file_names(directory):
    file_names = []
    for filename in os.listdir(directory):
        file_names.append(filename)
    return file_names


if __name__ == '__main__':
    print("-----Card OCR-----")
    image_path_list = [
        "unholy-heat-desc.jpg",
        "unholy-heat-footer-left.jpg",
        "unholy-heat-footer-right.jpg",
        "unholy-heat-top.jpg",
        "unholy-heat-type.jpg",
    ]

    for image_path in image_path_list:
        full_image_path = "images/" + image_path
        ocr_text = recognize_text(full_image_path)
        print(f"{image_path}:\n{ocr_text}\n-------\n")

    print("-----Symbol Matching-----")
    original_image_path = 'images/unholy-heat.jpeg'
    symbol_crop_image_path = 'images/unholy-heat-symbol.jpg'

    symbol_database_folder_path = 'images/symbol-database'
    symbol_path_list = get_file_names(symbol_database_folder_path)
    output_symbol_matching = []
    for symbol_path in symbol_path_list:
        match_sift = match_symbol_sift(symbol_crop_image_path, symbol_database_folder_path + "/" + symbol_path)
        match_orb = match_symbol_orb(symbol_crop_image_path, symbol_database_folder_path + "/" + symbol_path)
        output_symbol_matching.append((symbol_path, match_sift, match_orb))
        # match_surf = match_symbol_surf(original_image_path, symbol_database_folder_path + "/" + symbol_path)
        print("...")

    sorted_output_symbol_matching = sorted(output_symbol_matching, key=lambda x: x[1], reverse=True)

    for output in sorted_output_symbol_matching:
        symbol_path, match_sift, match_orb = output
        print(f"{symbol_path}: sift:{match_sift} orb:{match_orb}")

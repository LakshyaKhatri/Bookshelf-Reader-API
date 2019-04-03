import math
import cv2
import numpy as np
from PIL import Image
from io import BytesIO


def get_image_extension(django_image):
    "Returns image extension from a django image"
    pil_image = Image.open(django_image)
    return pil_image.format


def opencv_image_to_django_image(opencv_image, ext):
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
    django_image = BytesIO()

    pil_image = Image.fromarray(opencv_image)
    pil_image.save(django_image, format=ext)

    return django_image


def django_image_to_opencv_image(django_image):
    pil_image = Image.open(django_image)
    img = np.array(pil_image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


def removeDuplicateLines(sorted_points):
    last_x1 = 0
    non_duplicate_points = []
    for point in sorted_points:
        ((x1, y1), (x2, y2)) = point
        if last_x1 == 0:
            non_duplicate_points.append(point)
            last_x1 = x1

        elif abs(last_x1 - x1) >= 25:
            non_duplicate_points.append(point)
            last_x1 = x1

    return non_duplicate_points


def getPointsInXAndY(hough_lines, max_y):
    points = []
    for line in hough_lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + (max_y + 100) * (-b))
        y1 = int(y0 + (max_y + 100) * (a))
        start = (x1, y1)

        x2 = int(x0 - (max_y + 100) * (-b))
        y2 = int(y0 - (max_y + 100) * (a))
        end = (x2, y2)

        points.append((start, end))

    # Add a line at the very end of the image
    points.append(((500, max_y), (500, 0)))

    return points


def shortenLine(points, y_max):
    shortened_points = []
    for point in points:
        ((x1, y1), (x2, y2)) = point

        # Slope
        try:
            m = (y2 - y1) / (x2 - x1)
        except ZeroDivisionError:
            m = -1  # Infinite slope

        if m == -1:
            shortened_points.append(((x1, y_max), (x1, 0)))
            continue

        # From equation of line:
        # y-y1 = m (x-x1)
        # x = (y-y1)/m + x1
        # let y = y_max
        new_x1 = math.ceil(((y_max - y1) / m) + x1)
        start_point = (abs(new_x1), y_max)

        # Now let y = 0
        new_x2 = math.ceil(((0 - y1) / m) + x1)
        end_point = (abs(new_x2), 0)

        shortened_points.append((start_point, end_point))

    return shortened_points


def getCroppedImages(image, points):
    image = image.copy()
    y_max, _, _ = image.shape
    last_x1 = 0
    last_x2 = 0
    cropped_images = []

    for point in points:
        ((x1, y1), (x2, y2)) = point

        crop_points = np.array([[last_x1, y_max],
                                [last_x2, 0],
                                [x2, y2],
                                [x1, y1]])

        # Crop the bounding rect
        rect = cv2.boundingRect(crop_points)
        x, y, w, h = rect
        cropped = image[y: y + h, x: x + w].copy()

        # make mask
        crop_points = crop_points - crop_points.min(axis=0)
        mask = np.zeros(cropped.shape[:2], np.uint8)
        cv2.drawContours(mask, [crop_points], -1, (255, 255, 255), -1, cv2.LINE_AA)

        # do bit-op
        dst = cv2.bitwise_and(cropped, cropped, mask=mask)
        cropped_images.append(dst)

        last_x1 = x1
        last_x2 = x2

    return cropped_images


def reduceImageSize(img):
    img = img.copy()
    img_ht, img_wd, _ = img.shape
    ratio = img_wd / img_ht
    new_width = 500
    new_height = math.ceil(new_width / ratio)
    resized_image = cv2.resize(img, (new_width, new_height))

    return resized_image


def detectSpines(img):
    img = img.copy()
    height, width, _ = img.shape

    blur = cv2.GaussianBlur(img, (5, 5), 0)

    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    edge = cv2.Canny(gray, 50, 70)

    # kernel = np.ones((4, 1), np.uint8)
    kernel = np.array([[0, 0, 0, 0, 1, 0, 0, 0, 0],
                       [0, 0, 0, 0, 1, 0, 0, 0, 0],
                       [0, 0, 0, 0, 1, 0, 0, 0, 0],
                       [0, 0, 0, 0, 1, 0, 0, 0, 0],
                       [0, 0, 0, 0, 1, 0, 0, 0, 0]], dtype=np.uint8)

    img_erosion = cv2.erode(edge, kernel, iterations=1)

    lines = cv2.HoughLines(img_erosion, 1, np.pi / 180, 100)
    if lines is None:
        return []
    points = getPointsInXAndY(lines, height)
    points.sort(key=lambda val: val[0][0])
    non_duplicate_points = removeDuplicateLines(points)

    final_points = shortenLine(non_duplicate_points, height)

    return final_points


def getSpines(img):
    img = img.copy()
    final_image = reduceImageSize(img)
    final_points = detectSpines(final_image)
    cropped_images = getCroppedImages(final_image, final_points)
    return cropped_images


def drawSpineLines(django_image):
    img = django_image_to_opencv_image(django_image)
    ext = get_image_extension(django_image)

    final_image = reduceImageSize(img)
    final_points = detectSpines(final_image)

    for point in final_points:
        ((x1, y1), (x2, y2)) = point
        final_image = cv2.line(final_image, (x1, y1), (x2, y2), (0, 0, 255), 10)

    django_image = opencv_image_to_django_image(
        final_image,
        ext
    )
    return django_image, ext

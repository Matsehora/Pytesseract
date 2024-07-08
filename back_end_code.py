import cv2
import numpy as np


def invert_image(image):
    return cv2.bitwise_not(image)

def grayscale(image):
    return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

def binarize(image):
    trash, im_bw = cv2.threshold(image,150,255,cv2.THRESH_BINARY)
    return im_bw

def better_contrast(image,gamma):
    return np.uint8(cv2.pow(image / 255.0, gamma) * 255.0)

def noise_removal(image):
    
    kernel = np.ones((1,1),np.uint8)
    image = cv2.dilate(image,kernel,iterations=1)
    kernel = np.ones((1,1),np.uint8)
    image = cv2.erode(image,kernel,iterations=1)
    image = cv2.morphologyEx(image,cv2.MORPH_CLOSE,kernel) 
    image = cv2.medianBlur(image,3)
    return image

def thin_fog(image):
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.erode(image,kernel,iterations=1)
    image = cv2.bitwise_not(image)
    return image

def thick_fog(image):
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.dilate(image,kernel,iterations=1)
    image = cv2.bitwise_not(image)
    return image

def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    print (len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("temp/boxes.jpg", newImage)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle
# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

# Deskew image
def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)

def remove_bordesr(image):
    countours, hairche = cv2.findContours(image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cntSorted = sorted(countours, key = lambda x:cv2.contourArea(x))
    cnt = cntSorted[-1]
    x,y,w,h = cv2.boundingRect(cnt)
    crop = image[y:y+h,x:x+w]
    return(crop)


def missing_border(image):
    color = [255,255,255]
    top,botom,left,right = [150]*4

    image_witch_border = cv2.copyMakeBorder(image,top,botom,left,right,cv2.BORDER_CONSTANT,value=color)
    return image_witch_border

def image_processing(image,list_what_to_do: list,list_for_better_color:list, image_format):
    image = grayscale(image)
    list_for_better_color_copy = list_for_better_color.copy()
    cv2.imwrite(temp_format(image_format), image)
    if 1 < len(list_what_to_do):
        for functions in list_what_to_do[1:]:
            if functions == "better_contrast":
                function_to_call = globals()[functions]
                popped_element = list_for_better_color_copy.pop(0)
                image = function_to_call(image,popped_element)
            else:
                image = cv2.imread(temp_format(image_format))
                function_to_call = globals()[functions]
                print(function_to_call)
                image = function_to_call(image)
            cv2.imwrite(temp_format(image_format), image)

    return image
    
def temp_format(text: str):
    if text == 'PNG':
        return "temp_image.png"
    elif text == 'JPEG':
        return "temp_image.jpg"
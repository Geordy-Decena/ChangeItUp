import numpy as np
import cv2
import urllib.request


def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image


def get_radius(circles):
    radius = []
    for coords in circles[0, :]:
        radius.append(coords[2])
    return radius


def largest_radii(radii):
    largest_radii = 0
    print(radii)
    for i in radii:
        if(largest_radii < i):
            largest_radii = i

    return largest_radii


def av_pix(img, circles, size):
    av_value = []
    for coords in circles[0, :]:
        col = np.mean(img[coords[1]-size:coords[1]+size,
                          coords[0]-size:coords[0]+size])
        av_value.append(col)

    return av_value


def av_pixToonie(img, circles, size):
    av_value = []
    for coords in circles[0, :]:
        col = np.mean(img[coords[1]-size:coords[1]+size,
                          coords[0]-size:coords[0]+size])
        av_value.append(col)

    return av_value


def brightestLoonToon(loonToon, bright_values):
    brightest = 0
    for i in loonToon:
        if(brightest < bright_values[i]):
            brightest = bright_values[i]
    return brightest


url = "https://i.ibb.co/5Mrq2jd/coins7.jpg"

imgOG = url_to_image(url)

imgGray = cv2.cvtColor(imgOG, cv2.COLOR_BGR2GRAY)

# imgGray = cv2.imread("coins2.JPG", cv2.IMREAD_GRAYSCALE)
# imgOG = cv2.imread("coins2.JPG", 1)
# imgGray = cv2.GaussianBlur(imgGray, (5, 5), 0)

imgGray = cv2.blur(imgGray, (14, 14))

circles = cv2.HoughCircles(imgGray, cv2.HOUGH_GRADIENT, 1,
                           250, param1=50, param2=40, minRadius=170, maxRadius=370)

# imgGray = cv2.blur(imgGray, (2, 2))

# circles = cv2.HoughCircles(imgGray, cv2.HOUGH_GRADIENT, 1,
#                            150, param1=50, param2=40, minRadius=10, maxRadius=100)


print(circles)

count = 0

circles = np.uint16(np.around(circles))

for i in circles[0, :]:
    cv2.circle(imgOG, (i[0], i[1]), i[2], (0, 255, 0), 2)
    cv2.circle(imgOG, (i[0], i[1]), 2, (0, 0, 255), 3)
    cv2.putText(imgOG, str(count+1), (i[0], i[1]),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)

    count += 1


radii = get_radius(circles)
print(radii)

largest_radii = largest_radii(radii)
print(largest_radii)

bright_values = av_pix(imgGray, circles, largest_radii)
print(bright_values)

bright_valuesToonie = av_pix(imgGray, circles, 100)
print("BRIGHT TOONIE", bright_valuesToonie)

toonies = 0
loonies = 0
quarters = 0
dimes = 0
nickels = 0

# for i in radii:
#     temp = largest_radii/i
#     if(temp == 1 and temp < 1.11):
#         toonies += 1
#     if(temp >= 1.11 and temp < 1.24):
#         quarters += 1
#     if(temp >= 1.24 and temp < 1.45):
#         nickels += 1
#     if(temp >= 1.45):
#         dimes += 1

count = 0

loonToon = []

for i in radii:
    temp = largest_radii/i
    if(temp >= 1 and temp < 1.13):
        print("loonieToon", i)
        loonToon.append(count)
    if(temp >= 1.13 and temp < 1.25):
        print("quarter", i)
        quarters += 1
    if(temp >= 1.25 and temp < 1.45):
        print("nickel", i)
        nickels += 1
    if(temp >= 1.45):
        print("dime", i)
        dimes += 1
    count += 1

print("loonToon", loonToon)

brightestLoonToon = brightestLoonToon(loonToon, bright_values)
print(brightestLoonToon)

for i in loonToon:
    temp = bright_values[i]/bright_valuesToonie[i]
    if(temp > 1.08):
        toonies += 1
    else:
        loonies += 1

print(toonies, " ", loonies, " ", quarters, " ", dimes, " ", nickels)

value = toonies*2 + loonies + quarters*0.25 + nickels*0.05 + dimes*0.10

print("$", value)

cv2.imshow("imgOG", imgOG)

cv2.waitKey(0)
cv2.destroyAllWindows()

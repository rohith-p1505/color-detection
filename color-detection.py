import argparse
import cv2
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']
#Reading image with opencv
image = cv2.imread(img_path)

clicked = False
red = green = blue = x_position = y_position = 0

# Read color data from CSV into a pandas DataFrame
csv_columns = ["color", "color_name", "hex", "R", "G", "B"]
color_data = pd.read_csv('colors.csv', names=csv_columns, header=None)

def find_color_name(R, G, B):
    minimum_distance = 10000
    for i in range(len(color_data)):
        distance = abs(R - int(color_data.loc[i, "R"])) + abs(G - int(color_data.loc[i, "G"])) + abs(B - int(color_data.loc[i, "B"]))
        if distance <= minimum_distance:
            minimum_distance = distance
            color_name = color_data.loc[i, "color_name"]
    return color_name

def handle_mouse_click(event, x, y, flags, param):
    global blue, green, red, x_position, y_position, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        x_position = x
        y_position = y
        blue, green, red = image[y, x]
        blue = int(blue)
        green = int(green)
        red = int(red)

cv2.namedWindow('image')
cv2.setMouseCallback('image', handle_mouse_click)

while True:
    cv2.imshow("image", image)
    if clicked:
        cv2.rectangle(image, (20, 20), (750, 60), (blue, green, red), -1)
        color_info = find_color_name(red, green, blue) + ' R=' + str(red) + ' G=' + str(green) + ' B=' + str(blue)
        
        # Display color information on the image
        cv2.putText(image, color_info, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        
        # For very light colors, display text in black
        if red + green + blue >= 600:
            cv2.putText(image, color_info, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        clicked = False
    # exit when 'esc' key is pressed
    if cv2.waitKey(20) & 0xFF == 27:
        break

# Destroy all windows
cv2.destroyAllWindows()
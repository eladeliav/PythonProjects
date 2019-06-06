import cv2
import numpy as np

ERROR = 0.2
EPSILON = 200
current_x = 0
current_y = 0
clicked = False
hsv_click_color = [100, 100, 100]
low_offset = 60
high_offset = 60
found_ball = False


def on_mouse(event, x, y, flags, param):
    global current_x, current_y, clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        current_x = x
        current_y = y
        clicked = True
        print x, y


def nothing(_):
    pass


def clamp(val, max_value, min_value):
    return max(min(val, max_value), min_value)


def main():
    global clicked, hsv_click_color, low_offset, high_offset, found_ball
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Trackbars")
    cv2.namedWindow("Offset")
    cv2.createTrackbar("L - H", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("U - H", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("L - Offset", "Offset", low_offset, 255, nothing)
    cv2.createTrackbar("U - Offset", "Offset", high_offset, 255, nothing)

    cv2.namedWindow("Touchup")

    cv2.createTrackbar("Brush Size", "Touchup", 0, 10, nothing)
    cv2.createTrackbar("Operation", 'Touchup', 0, 4, nothing)
    cv2.createTrackbar("Iterations", "Touchup", 0, 10, nothing)

    while cv2.waitKey(1) != ord('q'):
        _, frame = cap.read()  # reading frame
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        if clicked:
            hsv_click_color = hsv[current_y, current_x]
            print hsv_click_color
            clicked = False

        # getting mask/touch up info from trackbars)
        low_offset = cv2.getTrackbarPos("L - Offset", "Offset")
        high_offset = cv2.getTrackbarPos("U - Offset", "Offset")

        # getting mask/touch up info from trackbars

        brush_size = cv2.getTrackbarPos("Brush Size", "Touchup")
        operation = cv2.getTrackbarPos("Operation", "Touchup")
        iterations = cv2.getTrackbarPos("Iterations", "Touchup")
        kernel = np.ones((brush_size, brush_size), np.uint8)  # setting brush size

        # highs and lows of chosen color range

        cv2.setTrackbarPos("L - H", "Trackbars", clamp(hsv_click_color[0] - low_offset, 255, 0))
        cv2.setTrackbarPos("L - S", "Trackbars", clamp(hsv_click_color[1] - low_offset, 255, 0))
        cv2.setTrackbarPos("L - V", "Trackbars", clamp(hsv_click_color[2] - low_offset, 255, 0))
        cv2.setTrackbarPos("U - H", "Trackbars", clamp(hsv_click_color[0] + high_offset, 255, 0))
        cv2.setTrackbarPos("U - S", "Trackbars", clamp(hsv_click_color[1] + high_offset, 255, 0))
        cv2.setTrackbarPos("U - V", "Trackbars", clamp(hsv_click_color[2] + high_offset, 255, 0))

        l_h = cv2.getTrackbarPos("L - H", "Trackbars")
        l_s = cv2.getTrackbarPos("L - S", "Trackbars")
        l_v = cv2.getTrackbarPos("L - V", "Trackbars")
        u_h = cv2.getTrackbarPos("U - H", "Trackbars")
        u_s = cv2.getTrackbarPos("U - S", "Trackbars")
        u_v = cv2.getTrackbarPos("U - V", "Trackbars")

        lower = np.array([l_h, l_s, l_v])
        upper = np.array([u_h, u_s, u_v])

        mask = cv2.inRange(hsv, lower, upper)  # mask for chosen color range

        erosion = cv2.erode(mask, kernel, iterations=iterations)  # defining possible effects
        dilation = cv2.dilate(mask, kernel, iterations=iterations)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=iterations)
        closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=iterations)

        if operation == 1:
            mask = cv2.bitwise_and(mask, mask, mask=erosion)
        if operation == 2:
            mask = cv2.bitwise_and(mask, mask, mask=dilation)
        if operation == 3:
            mask = cv2.bitwise_and(mask, mask, mask=opening)
        if operation == 4:
            mask = cv2.bitwise_and(mask, mask, mask=closing)

        result = cv2.bitwise_and(frame, frame, mask=mask)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # finding contours

        for contour in contours:
            area = cv2.contourArea(contour)  # contour area
            rect = cv2.minAreaRect(contour)  # creating bounding rectangle
            box = cv2.boxPoints(rect)  # getting box points
            box = np.int0(box)
            rect_area = cv2.contourArea(box)  # box area
            expected = 4 / np.pi  # expected ratio
            contour_x = box[0][0]
            contour_y = box[0][1]
            if area == 0 or area <= 1000:
                continue
            if abs((rect_area / area) - expected) <= ERROR:
                if ((current_x - contour_x) ** 2 + (current_y - contour_y) ** 2) ** 0.5 <= EPSILON:
                    #  print "Found ball thing in mouse click area (OOF)"
                    found_ball = True
                cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
                # cv2.rectangle(frame, tuple(box[0]), tuple(box[2]), (255, 0, 0), cv2.FILLED)

        cv2.imshow("frame", frame)  # raw frame (with shapes highlighted)
        cv2.imshow("result", result)  # frame with the mask
        cv2.setMouseCallback("frame", on_mouse)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

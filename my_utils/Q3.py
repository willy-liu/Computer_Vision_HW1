import cv2
from my_utils.my_pyqt5 import MainWindow


# 3.1 Stereo Disparity Map
def stereo_disparity_map(main_window: MainWindow):
    try:
        img_L = cv2.imread(main_window.Image_L_path)
        img_R = cv2.imread(main_window.Image_R_path)

        # Convert images to grayscale
        gray_L = cv2.cvtColor(img_L, cv2.COLOR_BGR2GRAY)
        gray_R = cv2.cvtColor(img_R, cv2.COLOR_BGR2GRAY)
        def update_disparity(val):
            numDisparities = cv2.getTrackbarPos('numDisparities', 'Disparity Map') * 16
            blockSize = cv2.getTrackbarPos('blockSize', 'Disparity Map')
            if blockSize % 2 == 0:
                blockSize += 1
            if blockSize < 5:
                blockSize = 5

            stereo = cv2.StereoBM.create(numDisparities=numDisparities, blockSize=blockSize)
            disparity = stereo.compute(gray_L, gray_R)
            disparity = cv2.normalize(disparity, disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            cv2.imshow('Disparity Map', disparity)

        cv2.namedWindow('Disparity Map')
        cv2.createTrackbar('numDisparities', 'Disparity Map', 1, 30, lambda val: update_disparity(max(1, min(val, 30))))
        cv2.createTrackbar('blockSize', 'Disparity Map', 5, 51, lambda val: update_disparity(max(5, min(val, 51))))

        # Set initial values
        cv2.setTrackbarPos('numDisparities', 'Disparity Map', 7)
        cv2.setTrackbarPos('blockSize', 'Disparity Map', 19)

        # Initial call to display the disparity map with default parameters
        update_disparity(0)

        cv2.imshow("img_L", img_L)
        cv2.imshow("img_R", img_R)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        main_window.show_message("Error", str(e))
    return

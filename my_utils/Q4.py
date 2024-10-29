import cv2
from my_utils.my_pyqt5 import MainWindow

#4.1 SIFT Keypoints
def sift_keypoints(main_window: MainWindow):
    try:
        img = cv2.imread(main_window.Image_1_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 創建SIFT檢測器並找到圖片的keypoints和descriptors
        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(gray, None)
        img = cv2.drawKeypoints(gray, keypoints, None, color=(0,255,0))


        cv2.imshow('SIFT Keypoints', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        main_window.show_message("Error", str(e))
    return

# 4.2 Matched Keypoints
def matched_keypoints(main_window: MainWindow):
    try:
        img1 = cv2.imread(main_window.Image_1_path)
        img2 = cv2.imread(main_window.Image_2_path)

        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # 創建SIFT檢測器並找到兩張圖片的keypoints和descriptors
        sift = cv2.SIFT_create()
        keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
        keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

        # 使用knnMatch找到最佳匹配
        matches = cv2.BFMatcher().knnMatch(descriptors1, descriptors2, k=2)
        good_matches = []
        for m, n in matches: # 若兩個最佳匹配的距離差異小於0.75，則視為好的匹配
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)
        
        img = cv2.drawMatches(img1, keypoints1, img2, keypoints2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        cv2.imshow('Matched Keypoints', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        main_window.show_message("Error", str(e))
    return
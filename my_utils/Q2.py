import cv2
import os

from my_utils.Q1 import *
from my_utils.my_pyqt5 import MainWindow

ORDER_POSITION = np.array([[7, 5, 0], [4, 5, 0], [1, 5, 0],
                          [7, 2, 0], [4, 2, 0], [1, 2, 0]])

######################################################

# 2.1 Show words on board
def show_words_on_board(main_window: MainWindow):
    try:
        folder_path = main_window.folder_path
        image_paths = sorted([f for f in os.listdir(folder_path) if f.endswith('.bmp')], key=lambda x: int(os.path.splitext(x)[0]))
        image_path = main_window.spinbox_extrinsic.currentText()

        # 從ar_text取得要顯示的字
        word = main_window.ar_text.toPlainText()
        word = word[:6] # 只取前6個字
        word = word.upper()

        fs = cv2.FileStorage(os.path.join(folder_path, 'Q2_db/alphabet_db_onboard.txt'), cv2.FILE_STORAGE_READ)
        all_corners = get_all_corners(folder_path, image_paths)  
        rmse, ins, dist, rvec, tvec = get_calibrateCamera(all_corners)

        for img_index, image_path in enumerate(image_paths):
            img = cv2.imread(os.path.join(folder_path, image_path))

            grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 依序將字寫上去
            for word_index, char in enumerate(word):
                charPoints = fs.getNode(char).mat().astype(np.float64).reshape(-1, 3)
                charPoints = charPoints + ORDER_POSITION[word_index] # 移動到對應的POSITION

                # @note PPT的參數順序有錯，計算那些點在圖片上的位置
                newCharPoints, _ = cv2.projectPoints(charPoints, rvec[img_index], tvec[img_index], ins, dist)
                newCharPoints = np.round(newCharPoints).astype(int).reshape(-1, 2, 2)

                for points in newCharPoints:
                    pointA = points[0]
                    pointB = points[1]
                    cv2.line(img, pointA, pointB, (0, 0, 255), 20)  # Added color argument

            cv2.imshow('image', img)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
    except Exception as e:
        main_window.show_message("Error", str(e))
    return

######################################################

# 2.2 Show words vertically
def show_words_vertically(main_window: MainWindow):
    try:
        folder_path = main_window.folder_path
        image_paths = sorted([f for f in os.listdir(folder_path) if f.endswith('.bmp')], key=lambda x: int(os.path.splitext(x)[0]))
        image_path = main_window.spinbox_extrinsic.currentText()

        # 從ar_text取得要顯示的字
        word = main_window.ar_text.toPlainText()
        word = word[:6] # 只取前6個字
        word = word.upper()

        fs = cv2.FileStorage(os.path.join(folder_path, 'Q2_db/alphabet_db_vertical.txt'), cv2.FILE_STORAGE_READ)
        all_corners = get_all_corners(folder_path, image_paths)  
        rmse, ins, dist, rvec, tvec = get_calibrateCamera(all_corners)

        for img_index, image_path in enumerate(image_paths):
            img = cv2.imread(os.path.join(folder_path, image_path))

            grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 依序將字寫上去
            for word_index, char in enumerate(word):
                charPoints = fs.getNode(char).mat().astype(np.float64).reshape(-1, 3)
                charPoints = charPoints + ORDER_POSITION[word_index] # 移動到對應的POSITION

                # @note PPT的參數順序有錯，計算那些點在圖片上的位置
                newCharPoints, _ = cv2.projectPoints(charPoints, rvec[img_index], tvec[img_index], ins, dist)
                newCharPoints = np.round(newCharPoints).astype(int).reshape(-1, 2, 2)

                for points in newCharPoints:
                    pointA = points[0]
                    pointB = points[1]
                    cv2.line(img, pointA, pointB, (0, 0, 255), 20)  # Added color argument

            cv2.imshow('image', img)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
    except Exception as e:
        main_window.show_message("Error", str(e))
    return

######################################################
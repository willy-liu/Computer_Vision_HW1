from my_utils.my_pyqt5 import MainWindow
from typing import Tuple

import cv2
import os
import numpy as np


# 1.1 Corner Detection

def get_corners(grayimg: np.ndarray) -> Tuple[bool, np.ndarray]:
    """得到棋盤格角點"""
    ret, corners = cv2.findChessboardCorners(grayimg, (11, 8))  # Adjust pattern size as needed
    if ret:
        winSize = (5, 5) # 搜索窗口的大小
        zeroZone = (-1, -1) # 死區大小，設置為 (-1, -1) 表示沒有死區。
        criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 0.001) # 終止條件，最多迭代 30 次或精度達到 0.001 時停止迭代

        corners = cv2.cornerSubPix(grayimg, corners, winSize, zeroZone, criteria) # 精細化角點的位置 

    return ret, corners

def get_all_corners(folder_path: str, image_paths: Tuple[str]) -> Tuple[np.ndarray]:
    corners = []
    for image_path in image_paths:
        img = cv2.imread(os.path.join(folder_path, image_path))
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corner = get_corners(grayimg)
        corners.append(corner)
    return np.array(corners)

def corner_detection(main_window: MainWindow):
    try:
        folder_path = main_window.folder_path
        image_paths = sorted([f for f in os.listdir(folder_path) if f.endswith('.bmp')], key=lambda x: int(os.path.splitext(x)[0]))

        for image_path in image_paths:
            img = cv2.imread(os.path.join(folder_path, image_path))
            
            grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 得到棋盤格角點
            ret, corners = get_corners(grayimg)
            # 畫出角點
            cv2.drawChessboardCorners(img, (11, 8), corners, ret)

            cv2.imshow(f'{image_path}', img)
            cv2.waitKey(1000)
            # cv2.setMouseCallback('image', lambda *args: None)
            cv2.destroyAllWindows()
    except Exception as e:
        main_window.show_message("Error", str(e))
    return

######################################################

# 1.2 Find the Intrinsic Matrix
def get_calibrateCamera(corners: np.ndarray) -> Tuple[float, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """得到校正相機的參數"""
    n = len(corners)

    # 用來表示棋盤格在世界坐標系中的三維座標
    objectPoints = np.zeros((11 * 8, 3), np.float32)
    # objectPoints: corners points of chessboard in 3D coordinate.(unit: 0.02m), (11x8x1)
    objectPoints[:, :2] = np.mgrid[0:11, 0:8].T.reshape(-1, 2) #* 0.02

    # 校正相機， @note 有5個回傳值才對
    # rmse 是校正的均方根誤差，ins 是內部相機矩陣，dist 是畸變係數，rvec 是旋轉向量，tvec 是平移向量
    rmse, ins, dist, rvec, tvec = cv2.calibrateCamera([objectPoints]*n, corners, (2048, 2048), None, None)

    return rmse, ins, dist, rvec, tvec

def find_the_intrinstic_matrix(main_window: MainWindow):
    try:
        folder_path = main_window.folder_path
        image_paths = sorted([f for f in os.listdir(folder_path) if f.endswith('.bmp')], key=lambda x: int(os.path.splitext(x)[0]))

        # 得到所有角點
        all_corners = get_all_corners(folder_path, image_paths)

        # 得到校正相機的參數
        rmse, ins, dist, rvec, tvec = get_calibrateCamera(all_corners)

        msg = f"Intrinsic: \n {ins}"
        main_window.show_message("Intrinsic Matrix", msg)
    except Exception as e:
        main_window.show_message("Error", str(e))
    return

######################################################

# 1.3 Find the Extrinsic Matrix
def find_extrinsic_matrix(main_window: MainWindow):
    try:
        folder_path = main_window.folder_path
        image_paths = sorted([f for f in os.listdir(folder_path) if f.endswith('.bmp')], key=lambda x: int(os.path.splitext(x)[0]))
        image_index = main_window.spinbox_extrinsic.currentText()
        img = cv2.imread(os.path.join(folder_path, image_paths[int(image_index)-1]))
        
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 得到所有角點
        all_corners = get_all_corners(folder_path, image_paths)

        # 得到校正相機的參數
        rmse, ins, dist, rvec, tvec = get_calibrateCamera(all_corners)

        # 將旋轉向量轉換為旋轉矩陣
        rotation_matrix = cv2.Rodrigues(rvec[0])[0]                 # @note rvec會是1X3X1的陣列，所以要用rvec[0]取出
        # 將旋轉矩陣與平移向量合併成外部相機參數
        extrinsic_matrix = np.hstack((rotation_matrix , tvec[0]))   # @note tvec同上

        msg = f"Extrinsic: \n {extrinsic_matrix}"
        main_window.show_message("Intrinsic Matrix", msg)
    except Exception as e:
        main_window.show_message("Error", str(e))
    return

######################################################

# 1.4 Find the Distortion Matrix
def find_distortion_matrix(main_window: MainWindow):
    try:
        folder_path = main_window.folder_path
        image_paths = sorted([f for f in os.listdir(folder_path) if f.endswith('.bmp')], key=lambda x: int(os.path.splitext(x)[0]))
        image_index = main_window.spinbox_extrinsic.currentText()
        img = cv2.imread(os.path.join(folder_path, image_paths[int(image_index)-1]))
        
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 得到所有角點
        all_corners = get_all_corners(folder_path, image_paths)

        # 得到校正相機的參數
        rmse, ins, dist, rvec, tvec = get_calibrateCamera(all_corners)

        msg = f"Distortion: \n {dist}"
        main_window.show_message("Distortion Matrix", msg)
    except Exception as e:
        main_window.show_message("Error", str(e))
    return

######################################################

# 1.5 Show the Undistorted Result
def show_undistorted_result(main_window: MainWindow):
    try:
        folder_path = main_window.folder_path
        image_paths = sorted([f for f in os.listdir(folder_path) if f.endswith('.bmp')], key=lambda x: int(os.path.splitext(x)[0]))
        image_index = main_window.spinbox_extrinsic.currentText()
        img = cv2.imread(os.path.join(folder_path, image_paths[int(image_index)-1]))
        
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 得到所有角點
        all_corners = get_all_corners(folder_path, image_paths)

        # 得到校正相機的參數
        rmse, ins, dist, rvec, tvec = get_calibrateCamera(all_corners)

        result_img = cv2.undistort(grayimg, ins, dist)

        cv2.imshow('Distorted image', img)
        cv2.imshow('Undistorted image', result_img)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()
    except Exception as e:
        main_window.show_message("Error", str(e))
    return

######################################################
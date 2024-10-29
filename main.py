import os
# 將工作目錄設為main.py的目錄，避免import不到
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

import sys
from PyQt5.QtWidgets import QApplication
from functools import partial

from my_utils.my_pyqt5 import MainWindow
from my_utils.Q1 import *
from my_utils.Q2 import *
from my_utils.Q3 import *
from my_utils.Q4 import *



# bind Q1 functions
def bind_Q1_functions(main_window: MainWindow):
    main_window.find_corners_btn.clicked.connect(partial(corner_detection, main_window))
    main_window.find_intrinsic_btn.clicked.connect(partial(find_the_intrinstic_matrix, main_window))
    main_window.find_extrinsic_btn.clicked.connect(partial(find_extrinsic_matrix, main_window))
    main_window.find_distortion_btn.clicked.connect(partial(find_distortion_matrix, main_window))
    main_window.show_result_btn.clicked.connect(partial(show_undistorted_result, main_window))

# bind Q2 functions
def bind_Q2_functions(main_window: MainWindow):
    main_window.show_words_board_btn.clicked.connect(partial(show_words_on_board, main_window))
    main_window.show_words_vertical_btn.clicked.connect(partial(show_words_vertically, main_window))

# bind Q3 functions
def bind_Q3_functions(main_window: MainWindow):
    main_window.stereo_disparity_btn.clicked.connect(partial(stereo_disparity_map, main_window))

# bind Q4 functions
def bind_Q4_functions(main_window: MainWindow):
    main_window.keypoints_btn.clicked.connect(partial(sift_keypoints, main_window))
    main_window.matched_keypoints_btn.clicked.connect(partial(matched_keypoints, main_window))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    
    # bind Question functions
    bind_Q1_functions(main_window)
    bind_Q2_functions(main_window)
    bind_Q3_functions(main_window)
    bind_Q4_functions(main_window)

    main_window.show()
    sys.exit(app.exec_())
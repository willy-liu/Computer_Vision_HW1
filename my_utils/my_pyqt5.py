import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QSpinBox, QTextEdit, QLabel, QVBoxLayout, QWidget, QGridLayout, QGroupBox, QHBoxLayout, QFileDialog, QComboBox
from PyQt5.QtWidgets import QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.folder_path = ""
        self.Image_L_path = ""
        self.Image_R_path = ""
        self.Image_1_path = ""
        self.Image_2_path = ""

        # Set main window title and size
        self.setWindowTitle("MainWindow - cvdlhw1.ui")
        self.setGeometry(100, 100, 900, 500)

        # Create central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a grid layout
        layout = QGridLayout()

        # Load Image Section
        load_group = QGroupBox("Load Image")
        load_layout = QVBoxLayout()
        load_folder_btn = QPushButton("Load folder")
        loaded_folder_label = QLabel("")
        loaded_folder_label.setWordWrap(True)
        load_image_L_btn = QPushButton("Load Image_L")
        loaded_image_L_label = QLabel("")
        load_image_R_btn = QPushButton("Load Image_R")
        loaded_image_R_label = QLabel("")

        def load_folder():
            self.folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
            # loaded_folder_label.setText(f"Loaded folder: \n{self.folder_path}")
            loaded_folder_label.setText(f"{self.folder_path}")
            if self.folder_path:
                print(f"Selected folder: {self.folder_path}")

        def load_image(image_type):
            if image_type == "L":
                self.Image_L_path, _ = QFileDialog.getOpenFileName(self, "Select Image_L", "", "Image Files (*.png *.jpg *.bmp)")
                loaded_image_L_label.setText(f"{self.Image_L_path.split('/')[-1]}")
                if self.Image_L_path:
                    print(f"Selected Image_L: {self.Image_L_path}")
            elif image_type == "R":
                self.Image_R_path, _ = QFileDialog.getOpenFileName(self, "Select Image_R", "", "Image Files (*.png *.jpg *.bmp)")
                loaded_image_R_label.setText(f"{self.Image_R_path.split('/')[-1]}")
                if self.Image_R_path:
                    print(f"Selected Image_R: {self.Image_R_path}")
            elif image_type == "1":
                self.Image_1_path, _ = QFileDialog.getOpenFileName(self, "Select Image1", "", "Image Files (*.png *.jpg *.bmp)")
                loaded_image_1_label.setText(f"{self.Image_1_path.split('/')[-1]}")
                if self.Image_1_path:
                    print(f"Selected Image1: {self.Image_1_path}")
            elif image_type == "2":
                self.Image_2_path, _ = QFileDialog.getOpenFileName(self, "Select Image2", "", "Image Files (*.png *.jpg *.bmp)")
                loaded_image_2_label.setText(f"{self.Image_2_path.split('/')[-1]}")
                if self.Image_2_path:
                    print(f"Selected Image2: {self.Image_2_path}")

        load_folder_btn.clicked.connect(load_folder)
        load_image_L_btn.clicked.connect(lambda: load_image("L"))
        load_image_R_btn.clicked.connect(lambda: load_image("R"))

        load_layout.addWidget(load_folder_btn)
        load_layout.addWidget(loaded_folder_label)
        load_layout.addWidget(load_image_L_btn)
        load_layout.addWidget(loaded_image_L_label)
        load_layout.addWidget(load_image_R_btn)
        load_layout.addWidget(loaded_image_R_label)
        load_group.setLayout(load_layout)
        layout.addWidget(load_group, 0, 0)

        # 1. Calibration Section
        calibration_group = QGroupBox("1. Calibration")
        calibration_layout = QVBoxLayout()
        self.find_corners_btn = QPushButton("1.1 Find corners")
        self.find_intrinsic_btn = QPushButton("1.2 Find intrinsic")
        self.find_extrinsic_btn = QPushButton("1.3 Find extrinsic")
        find_extrinsic_group = QGroupBox("1.3 Find extrinsic")
        self.find_distortion_btn = QPushButton("1.4 Find distortion")
        self.show_result_btn = QPushButton("1.5 Show result")
        calibration_layout.addWidget(self.find_corners_btn)
        calibration_layout.addWidget(self.find_intrinsic_btn)
        find_extrinsic_layout = QVBoxLayout()
        find_extrinsic_group.setLayout(find_extrinsic_layout)
        self.spinbox_extrinsic = QComboBox()
        self.spinbox_extrinsic.addItems([str(i) for i in range(1, 16)])
        find_extrinsic_layout.addWidget(self.spinbox_extrinsic)
        find_extrinsic_layout.addWidget(self.find_extrinsic_btn)
        calibration_layout.addWidget(find_extrinsic_group)
        calibration_layout.addWidget(self.find_distortion_btn)
        calibration_layout.addWidget(self.show_result_btn)
        calibration_group.setLayout(calibration_layout)
        layout.addWidget(calibration_group, 0, 1)

        # 2. Augmented Reality Section
        ar_group = QGroupBox("2. Augmented Reality")
        ar_layout = QVBoxLayout()
        self.ar_text = QTextEdit()
        self.ar_text.setFixedHeight(30)  # Set fixed height for ar_text
        self.show_words_board_btn = QPushButton("2.1 show words on board")
        self.show_words_vertical_btn = QPushButton("2.2 show words vertical")
        ar_layout.addWidget(self.ar_text)
        ar_layout.addWidget(self.show_words_board_btn)
        ar_layout.addWidget(self.show_words_vertical_btn)
        ar_group.setLayout(ar_layout)
        layout.addWidget(ar_group, 0, 2)

        # 3. Stereo Disparity Map Section
        stereo_group = QGroupBox("3. Stereo disparity map")
        stereo_layout = QVBoxLayout()
        self.stereo_disparity_btn = QPushButton("3.1 stereo disparity map")
        stereo_layout.addWidget(self.stereo_disparity_btn)
        stereo_group.setLayout(stereo_layout)
        layout.addWidget(stereo_group, 0, 3)

        # 4. SIFT Section
        sift_group = QGroupBox("4. SIFT")
        sift_layout = QVBoxLayout()
        load_image_1_btn = QPushButton("Load Image1")
        loaded_image_1_label = QLabel("")
        load_image_2_btn = QPushButton("Load Image2")
        loaded_image_2_label = QLabel("")
        self.keypoints_btn = QPushButton("4.1 Keypoints")
        self.matched_keypoints_btn = QPushButton("4.2 Matched Keypoints")
        sift_layout.addWidget(load_image_1_btn)
        sift_layout.addWidget(loaded_image_1_label)
        sift_layout.addWidget(load_image_2_btn)
        sift_layout.addWidget(loaded_image_2_label)
        sift_layout.addWidget(self.keypoints_btn)
        sift_layout.addWidget(self.matched_keypoints_btn)
        sift_group.setLayout(sift_layout)
        layout.addWidget(sift_group, 1, 1)

        load_image_1_btn.clicked.connect(lambda: load_image("1"))
        load_image_2_btn.clicked.connect(lambda: load_image("2"))

        # 5. VGG19 Section
        # vgg19_group = QGroupBox("5. VGG19")
        # vgg19_layout = QVBoxLayout()
        # self.load_image_vgg19_btn = QPushButton("Load Image")
        # self.show_augmented_images_btn = QPushButton("5.1 Show Augmented Images")
        # self.show_model_structure_btn = QPushButton("5.2 Show Model Structure")
        # self.show_acc_loss_btn = QPushButton("5.3 Show Acc and Loss")
        # self.inference_btn = QPushButton("5.4 Inference")
        # predict_label = QLabel("Predict =")
        # self.inference_result_text = QTextEdit()

        # vgg19_layout.addWidget(self.load_image_vgg19_btn)
        # vgg19_layout.addWidget(self.show_augmented_images_btn)
        # vgg19_layout.addWidget(self.show_model_structure_btn)
        # vgg19_layout.addWidget(self.show_acc_loss_btn)
        # vgg19_layout.addWidget(self.inference_btn)
        # vgg19_layout.addWidget(predict_label)
        # vgg19_layout.addWidget(self.inference_result_text)
        # vgg19_group.setLayout(vgg19_layout)
        # layout.addWidget(vgg19_group, 1, 2)

        # Set layout to the central widget
        central_widget.setLayout(layout)

    
    def bind_btn(self, btn, func):
        btn.clicked.connect(func)

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title) # Mac不會顯示標題
        msg_box.setText(message)
        msg_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    # main_window.bind_btn(main_window.find_corners_btn, lambda: main_window.show_message("Find Corners", "Find Corners"))
    main_window.show()
    sys.exit(app.exec_())
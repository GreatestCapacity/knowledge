from PyQt5.QtWidgets import QWidget, QHBoxLayout, QToolBar, QVBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox
from .LeftTabView import LeftTabView
from .MainFrame import MainFrame


class MainWindow(QWidget):
    new_note_btn = None
    edit_btn = None
    save_btn = None
    cancel_btn = None
    left_tab_view = None
    main_frame = None

    def __init__(self):
        super().__init__()

        # Base Layout
        v_layout = QVBoxLayout()
        self.setLayout(v_layout)

        # Tool Bar
        tool_bar = QToolBar()
        v_layout.addWidget(tool_bar)

        # New Note Button on Tool Bar
        self.new_note_btn = QPushButton('New Note', tool_bar)
        self.new_note_btn.clicked.connect(self.new_note_clicked)
        tool_bar.addWidget(self.new_note_btn)

        # Edit Button on Tool Bar
        self.edit_btn = QPushButton('Edit', tool_bar)
        self.edit_btn.clicked.connect(self.edit_clicked)
        self.edit_btn.setDisabled(True)
        tool_bar.addWidget(self.edit_btn)

        # Save Button on Tool Bar
        self.save_btn = QPushButton('Save', tool_bar)
        self.save_btn.clicked.connect(self.save_clicked)
        self.save_btn.setDisabled(True)
        tool_bar.addWidget(self.save_btn)

        # Cancel Button on Tool Bar
        self.cancel_btn = QPushButton('Cancel', tool_bar)
        self.cancel_btn.clicked.connect(self.cancel_clicked)
        self.cancel_btn.setDisabled(True)
        tool_bar.addWidget(self.cancel_btn)

        # Main Layout in Base Layout
        self.h_layout = QHBoxLayout()
        v_layout.addLayout(self.h_layout)

        # Left Tab Tree View in Main Layout
        self.left_tab_view = LeftTabView(self)
        self.left_tab_view.on_note_selected(self.note_selected)
        self.h_layout.addWidget(self.left_tab_view)
        self.h_layout.setStretch(0, 2)

        # Main Frame in Main Layout
        self.main_frame = MainFrame(self)
        self.h_layout.addWidget(self.main_frame)
        self.h_layout.setStretch(1, 10)

        # Window Settings
        self.setGeometry(300, 300, 1500, 800)
        self.setWindowTitle('Knowledge')
        self.show()

    # Receive Note Selected Signal from LeftTabView
    def note_selected(self, note_title):
        # Enable Edit Button on ToolBar
        self.edit_btn.setEnabled(True)

        # Show Note's Content in Main Frame
        self.main_frame.show_note(note_title)

        print(note_title)

    def enter_editing(self):
        # Disable New Note and Edit Button on ToolBar
        self.new_note_btn.setDisabled(True)
        self.edit_btn.setDisabled(True)

        # Disable LeftTabView's Operate Access
        self.left_tab_view.setVisible(False)

        # Enable Save and Cancel Button on ToolBar
        self.save_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)

    def exit_editing(self):
        # Enable New Note and Edit Button on ToolBar
        self.new_note_btn.setEnabled(True)
        self.edit_btn.setEnabled(True)

        # Enable Left TabView's Operate Access
        self.left_tab_view.setVisible(True)

        # Disable Save and Cancel Button on ToolBar
        self.save_btn.setDisabled(True)
        self.cancel_btn.setDisabled(True)

    def new_note_clicked(self):
        self.enter_editing()
        self.main_frame.new_note()

    def edit_clicked(self):
        self.enter_editing()
        self.main_frame.edit_note()

    def save_clicked(self):
        if self.main_frame.save_note():
            self.exit_editing()
            self.left_tab_view.refresh_data()

    def cancel_clicked(self):
        self.main_frame.edit_cancel()
        self.exit_editing()

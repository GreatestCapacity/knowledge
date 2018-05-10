from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QPushButton, QWidget
from .NotebookTreeView import NotebookTreeView
from .TagTreeView import TagTreeView


class LeftTabView(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Notebook Tab
        self.notebook_tree_widget = QWidget(self)
        self.addTab(self.notebook_tree_widget, 'Notebook')

        # Notebook Tab Vertical Layout
        self.notebook_v_layout = QVBoxLayout()
        self.notebook_tree_widget.setLayout(self.notebook_v_layout)

        # Add Notebook Button
        self.add_notebook_btn = QPushButton(self)
        self.add_notebook_btn.setText('Add Notebook')
        self.add_notebook_btn.clicked.connect(self.add_notebook)
        self.notebook_v_layout.addWidget(self.add_notebook_btn)

        # NotebookTreeView
        self.notebook_tree_view = NotebookTreeView(self)
        self.notebook_v_layout.addWidget(self.notebook_tree_view)

        # Tag Tab
        self.tag_tree_widget = QWidget(self)
        self.addTab(self.tag_tree_widget, 'Tag')

        # Tag Tab Vertical Layout
        self.tag_v_layout = QVBoxLayout()
        self.tag_tree_widget.setLayout(self.tag_v_layout)

        # Add Tag Button
        self.add_tag_btn = QPushButton(self)
        self.add_tag_btn.setText('Add Tag')
        self.add_tag_btn.clicked.connect(self.add_tag)
        self.tag_v_layout.addWidget(self.add_tag_btn)

        # TagTreeView
        self.tag_tree_view = TagTreeView(self)
        self.tag_v_layout.addWidget(self.tag_tree_view)

    def add_notebook(self):
        self.notebook_tree_view.add_root_item()

    def add_tag(self):
        self.tag_tree_view.add_root_item()

    # Send Note Selected Signal to MainWindow
    def on_note_selected(self, func):
        self.notebook_tree_view.note_selected = func
        self.tag_tree_view.note_selected = func

    # Receive Data Refresh Signal from MainWindow
    def refresh_data(self):
        self.notebook_tree_view.refresh_data()
        self.tag_tree_view.refresh_data()

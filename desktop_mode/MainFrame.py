from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QComboBox
from lib.database import engine, Note
from lib.data_access import DataAccess
from .MarkdownView import MarkdownView
from .MarkdownEditor import MarkdownEditor


class MainFrame(QWidget):
    data_access = DataAccess(engine)
    title_input = None
    notebook_selector = None
    markdown_view = None
    markdown_editor = None
    note = None
    note_editing = None

    def __init__(self, parent=None):
        super().__init__(parent)

        # Base Vertical layout
        v_layout = QVBoxLayout()
        self.setLayout(v_layout)

        # Title Input
        self.title_input = QLineEdit(self)
        self.title_input.setDisabled(True)
        v_layout.addWidget(self.title_input)

        # Notebook Select
        property_h_layout = QHBoxLayout()
        v_layout.addLayout(property_h_layout)

        # Select Notebook Label
        notebook_select_label = QLabel('Select Notebook', self)
        property_h_layout.addWidget(notebook_select_label)

        # Select Notebook Combo Box
        self.notebook_selector = QComboBox(self)
        self.notebook_selector.addItems([notebook.name for notebook in self.data_access.list_notebooks()])
        self.notebook_selector.setDisabled(True)
        property_h_layout.addWidget(self.notebook_selector)

        # Horizontal layout to show and edit note content
        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)

        # Markdown View in Horizontal Layout
        self.markdown_view = MarkdownView(self)
        h_layout.addWidget(self.markdown_view)

        # Markdown Editor in Horizontal Layout
        self.markdown_editor = MarkdownEditor(self)
        self.markdown_editor.setVisible(False)
        self.markdown_editor.set_editing_callback(self.editing_callback)
        h_layout.addWidget(self.markdown_editor)

    def enter_editing(self):
        # Enable Title Input
        self.title_input.setEnabled(True)
        self.title_input.setText(self.note_editing.title)

        # Enable and Refresh Notebook Selector
        self.notebook_selector.setEnabled(True)
        self.notebook_selector.clear()
        self.notebook_selector.addItems([notebook.name for notebook in self.data_access.list_notebooks()])
        if self.note:
            self.notebook_selector.setCurrentText(self.note.notebook.name)

        # Show MarkdownEditor
        self.markdown_editor.setVisible(True)
        self.markdown_editor.edit_note(self.note_editing.content)

        # Show Editing Content in MarkdownView
        self.markdown_view.show_note(self.note_editing.content)

    def exit_editing(self):
        # Disable Title Input
        self.title_input.setDisabled(True)
        if self.note:
            self.title_input.setText(self.note.title)
        else:
            self.title_input.setText('')

        # Disable Notebook Selector
        self.notebook_selector.setDisabled(True)

        # Close MarkdownEditor
        self.markdown_editor.setVisible(False)

        # Show Current Note Content in MarkdownView
        if self.note:
            self.markdown_view.show_note(self.note.content)
        else:
            self.markdown_view.show_default_page()

    # Receive Editing Signal from MarkdownEditor
    def editing_callback(self, content):
        self.note_editing.content = content
        self.markdown_view.show_note(content)

    # Receive signals from MainWindow
    def show_note(self, note_title):
        if self.data_access.has_note(note_title):
            self.note = self.data_access.get_note_by_title(note_title)
            self.notebook_selector.setCurrentText(self.note.notebook.name)
            self.markdown_view.show_note(self.note.content)
        else:
            self.markdown_view.show_default_page()

    def new_note(self):
        self.note_editing = Note()
        self.note_editing.title = ''
        self.note_editing.content = ''
        self.enter_editing()

    def edit_note(self):
        self.note_editing = self.note
        self.enter_editing()

    def save_note(self):
        if self.title_input.text() != '' and self.markdown_editor.toPlainText() != '':
            notebook_name = self.notebook_selector.currentText()
            notebook = self.data_access.get_notebook_by_name(notebook_name)
            self.note = self.note_editing
            self.note.title = self.title_input.text()
            self.note.notebook = notebook
            self.data_access.save_note(self.note)
            self.exit_editing()
            return True
        else:
            return False

    def edit_cancel(self):
        self.exit_editing()

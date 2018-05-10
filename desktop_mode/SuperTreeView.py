from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QAction, QAbstractItemView, QStyledItemDelegate
from PyQt5.QtCore import Qt, QPoint, QFile, QMimeData, QVariant, QDataStream, QIODevice
from PyQt5.QtGui import QCursor, QDropEvent, QDragEnterEvent, QDragMoveEvent, QDrag, QFont
from lib.database import engine
from lib.data_access import DataAccess
import os


class SuperTreeView(QTreeWidget):
    def __init__(self, source, parent=None):
        super().__init__(parent)

        self.setHeaderHidden(True)

        # Enable Drag and Drop
        self.setDefaultDropAction(Qt.MoveAction)
        self.setDragDropMode(QAbstractItemView.DragDrop)

        # Load StyleSheet
        path = os.getcwd()
        print(path)
        stylesheet_file = QFile(path + "/desktop_mode/stylesheet.qss")
        if stylesheet_file.open(QFile.ReadOnly):
            self.setStyleSheet(str(stylesheet_file.readAll(), encoding='utf-8'))
            stylesheet_file.close()
            print('Use stylesheet successfully')

        # Set Item Clicked Slot
        self.itemClicked.connect(self.item_clicked)

        # Set Item Right Clicked Slot
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.item_right_clicked)

        # Set All Data in Tree
        for item in source:
            tree_item = QTreeWidgetItem([item.name])
            tree_item.setFlags(tree_item.flags() | Qt.ItemIsEditable)
            for note in item.note:
                sub_tree_item = QTreeWidgetItem(tree_item)
                sub_tree_item.setText(0, note.title)
                sub_tree_item.setFlags(sub_tree_item.flags() | Qt.ItemIsEditable)
            self.addTopLevelItem(tree_item)

        # Set Edit Finished Slot
        item_delegate = QStyledItemDelegate(self)
        self.setItemDelegate(item_delegate)
        item_delegate.closeEditor.connect(self.rename_finished)

        # Set Item Double Clicked Slot
        self.itemDoubleClicked.connect(self.rename_item)

        # Record name to rename
        self.old_name = ''
        self.new_name = ''

    # Can Only Drag Sub Item
    def startDrag(self, supported_actions):
        current_item = self.currentItem()
        if current_item.parent():
            super().startDrag(supported_actions)

    # When drag on blank area or note item, show forbidden icon
    def dragMoveEvent(self, event: QDragMoveEvent):
        current_item = self.itemAt(event.pos())
        if not current_item or current_item.parent():
            event.ignore()
        else:
            super().dragMoveEvent(event)

    # Drop a note to a notebook then calling DataAccess.move_note_notebook()
    def dropEvent(self, event: QDropEvent):
        if self.dropIndicatorPosition() == 0:
            print('Note:', self.currentItem().text(0))
            print('Notebook:', self.itemAt(event.pos()).text(0))
            notebook_name = self.itemAt(event.pos()).text(0)
            note_title = self.currentItem().text(0)
            data_access = DataAccess(engine)
            if data_access.has_notebook(notebook_name) and data_access.has_note(note_title):
                notebook = data_access.get_notebook_by_name(notebook_name)
                note = data_access.get_note_by_title(note_title)
                data_access.move_note_to_notebook(note, notebook)
                super().dropEvent(event)

    # Click a root item will expand it, click a note will send to MainWindow
    def item_clicked(self, item: QTreeWidgetItem, column):
        if item.parent():
            print('item clicked', item.text(0))
            self.note_selected(item.text(0))
        else:
            item.setExpanded(not item.isExpanded())

    # Right Click Menu
    def item_right_clicked(self, pos: QPoint):
        print('right clicked')
        current_item = self.itemAt(pos)
        if current_item:
            print(self.itemAt(pos).text(0))
            menu = QMenu()
            menu.addAction('Rename', self.rename_item)
            menu.addAction('Delete', self.delete_item)
            menu.exec(QCursor.pos())

    # Double Click a Item or Click Rename in Right Menu
    # Record Old Name of Current Item
    def rename_item(self):
        self.old_name = self.currentItem().text(0)
        self.editItem(self.currentItem())

    # Called When Rename Finished
    def rename_finished(self):
        self.new_name = self.currentItem().text(0)
        if self.old_name != self.new_name:
            if self.currentItem().parent():
                self.rename_note(self.old_name, self.new_name)
            else:
                self.rename_root_item(self.old_name, self.new_name)

    # Rename Note by DataAccess
    def rename_note(self, old_name, new_name):
        print('Rename Note:', old_name, 'to', new_name)
        data_access = DataAccess(engine)
        if not data_access.has_note(new_name):
            note = data_access.get_note_by_title(old_name)
            note.title = new_name
            data_access.save_note(note)
        else:
            self.editItem(self.currentItem())

    # Virtual Method Implement By Child Class
    # Notebook will rename notebook and Tag will rename tag
    def rename_root_item(self, old_name, new_name):
        return

    # Click Delete in Right Menu
    def delete_item(self):
        current_item = self.currentItem()
        if current_item.parent():
            self.delete_note(current_item.text(0))
        else:
            self.delete_root_item(current_item.text(0))

    # Delete Note by DataAccess
    def delete_note(self, note_title):
        print('Delete_Note:', note_title)
        data_access = DataAccess(engine)
        note = data_access.get_note_by_title(note_title)
        data_access.delete_note(note)
        self.currentItem().removeChild(self.currentItem())

    # Virtual Method Implement By Child Class
    # Notebook will delete notebook and Tag will delete tag
    def delete_root_item(self, root_item_name):
        return

    def add_root_item(self):
        item = QTreeWidgetItem(self, ['New Item'])
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.addTopLevelItem(item)
        self.setCurrentItem(item)
        self.editItem(item)

    def refresh_data(self, source):
        self.clear()

        # Set All Data in Tree
        for item in source:
            tree_item = QTreeWidgetItem([item.name])
            tree_item.setFlags(tree_item.flags() | Qt.ItemIsEditable)
            for note in item.note:
                sub_tree_item = QTreeWidgetItem(tree_item)
                sub_tree_item.setText(0, note.title)
                sub_tree_item.setFlags(sub_tree_item.flags() | Qt.ItemIsEditable)
            self.addTopLevelItem(tree_item)

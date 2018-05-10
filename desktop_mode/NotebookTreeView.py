from lib.database import engine
from lib.data_access import DataAccess
from .SuperTreeView import SuperTreeView


class NotebookTreeView(SuperTreeView):
    def __init__(self, parent=None):
        self.data_access = DataAccess(engine)
        notebooks = self.data_access.list_notebooks()

        super().__init__(notebooks, parent)

    # Refresh Data
    def refresh_data(self):
        notebooks = self.data_access.list_notebooks()
        super().refresh_data(notebooks)

    # Rename Notebook
    def rename_root_item(self, old_name, new_name):
        print('Rename Notebook', old_name, 'to', new_name)
        if not self.data_access.has_notebook(new_name):
            if self.data_access.has_notebook(old_name):
                notebook = self.data_access.get_notebook_by_name(old_name)
                notebook.name = new_name
                self.data_access.save_notebook(notebook)
            else:
                self.data_access.add_notebook(new_name)
        else:
            self.editItem(self.currentItem())

    # Delete Notebook
    def delete_root_item(self, notebook_name):
        if self.data_access.has_notebook(notebook_name):
            notebook = self.data_access.get_notebook_by_name(notebook_name)
            self.data_access.delete_notebook(notebook)
            self.currentItem().removeChild(self.currentItem())
            print('Delete Notebook', notebook_name)

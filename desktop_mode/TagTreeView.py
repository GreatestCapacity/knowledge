from lib.database import engine
from lib.data_access import DataAccess
from .SuperTreeView import SuperTreeView


class TagTreeView(SuperTreeView):
    def __init__(self, parent=None):
        self.old_name = ''
        self.new_name = ''

        self.data_access = DataAccess(engine)
        tags = self.data_access.list_tags()

        super().__init__(tags, parent)

        # Cannot drag a note to a tag
        self.setDragEnabled(False)

    # Refresh Data
    def refresh_data(self):
        tags = self.data_access.list_tags()
        super().refresh_data(tags)

    # Rename Tag
    def rename_root_item(self, old_name, new_name):
        print('Rename Tag', old_name, 'to', new_name)
        if not self.data_access.has_tag(new_name):
            if self.data_access.has_tag(old_name):
                tag = self.data_access.get_tag_by_name(old_name)
                tag.name = new_name
                self.data_access.save_tag(tag)
            else:
                self.data_access.add_tag(new_name)
        else:
            self.editItem(self.currentItem())

    # Delete Tag
    def delete_root_item(self, tag_name):
        if self.data_access.has_tag(tag_name):
            tag = self.data_access.get_tag_by_name(tag_name)
            self.data_access.delete_tag(tag)
            self.currentItem().removeChild(self.currentItem())
            print('Delete Tag', tag_name)

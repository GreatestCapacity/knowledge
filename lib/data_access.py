from sqlalchemy.orm import sessionmaker
from .database import Notebook, Note, Tag, Image


class DataAccess:
    def __init__(self, engine):
        self.engine = engine
        self.session = sessionmaker(bind=self.engine)()

    # insert

    # str -> ()
    def add_notebook(self, name):
        notebook = Notebook(name=name)
        self.session.add(notebook)
        self.session.commit()

    # str -> ()
    def add_tag(self, name):
        tag = Tag(name=name)
        self.session.add(tag)
        self.session.commit()

    # str, str, Notebook -> ()
    def add_note(self, title, content, notebook):
        note = Note(title=title, content=content, notebook_id=notebook.id)
        self.session.add(note)
        self.session.commit()

    # byte -> ()
    def add_image(self, content):
        return

    # delete

    # Notebook -> ()
    def delete_notebook(self, notebook):
        self.session.delete(notebook)
        self.session.commit()

    # Tag -> ()
    def delete_tag(self, tag):
        self.session.delete(tag)
        self.session.commit()

    # Note -> ()
    def delete_note(self, note):
        self.session.delete(note)
        self.session.commit()

    # Image -> ()
    def delete_image(self, image):
        return

    # modify

    # Notebook -> ()
    def save_notebook(self, notebook):
        self.session.add(notebook)
        self.session.commit()

    # Tag -> ()
    def save_tag(self, tag):
        self.session.add(tag)
        self.session.commit()

    # Note -> ()
    def save_note(self, note):
        self.session.add(note)
        self.session.commit()

    # query

    # () -> Generator(Notebook)
    def list_notebooks(self):
        for notebook in self.session.query(Notebook):
            yield notebook

    # str -> bool
    def has_notebook(self, name):
        return self.session.query(Notebook).filter_by(name=name).count() != 0

    # str -> Notebook
    def get_notebook_by_name(self, name):
        return self.session.query(Notebook).filter_by(name=name).one()

    # str -> Generator(Tag)
    def list_tags(self):
        for tag in self.session.query(Tag):
            yield tag

    # str -> bool
    def has_tag(self, name):
        return self.session.query(Tag).filter_by(name=name).count() != 0

    # str -> Tag
    def get_tag_by_name(self, name):
        return self.session.query(Tag).filter_by(name=name).one()

    # () -> Generator(Note)
    def list_all_notes(self):
        for note in self.session.query(Note):
            yield note

    # str -> bool
    def has_note(self, title):
        return self.session.query(Note).filter_by(title=title).count() != 0

    # str -> Notebook
    def get_note_by_title(self, title):
        return self.session.query(Note).filter_by(title=title).one()

    # relationship

    # Note, Tag -> ()
    def link_note_with_tag(self, note, tag):
        note.tag.append(tag)
        self.session.add(note)
        self.session.commit()

    # Note, Tag -> ()
    def unlink_note_with_tag(self, note, tag):
        note.tag.remove(tag)
        self.session.add(note)
        self.session.commit()

    # Note, Notebook -> ()
    def move_note_to_notebook(self, note, notebook):
        note.notebook_id = notebook.id
        self.session.add(note)
        self.session.commit()

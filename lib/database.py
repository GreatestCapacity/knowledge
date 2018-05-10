from sqlalchemy import create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, LargeBinary, TIMESTAMP
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now, current_timestamp
from config import db_conn_url

engine = create_engine(db_conn_url)

Base = declarative_base()

note_tag = Table(
        'note_tag', Base.metadata,
        Column('note.id', Integer, ForeignKey('note.id')),
        Column('tag.id', Integer, ForeignKey('tag.id'))
        )

note_img = Table(
        'note_img', Base.metadata,
        Column('note.id', Integer, ForeignKey('note.id')),
        Column('image.id', Integer, ForeignKey('image.id'))
        )


class Notebook(Base):
    __tablename__ = 'notebook'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    note = relationship('Note', back_populates='notebook',
                        cascade='all, delete, delete-orphan')


class Note(Base):
    __tablename__ = 'note'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    content = Column(Text, default='')
    create_time = Column(TIMESTAMP, default=now())
    last_modified = Column(TIMESTAMP, default=now(), onupdate=current_timestamp())
    notebook_id = Column(Integer, ForeignKey('notebook.id'))
    notebook = relationship('Notebook', back_populates='note')
    tag = relationship('Tag', secondary=note_tag, back_populates='note')


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    note = relationship('Note', secondary=note_tag, back_populates='tag')



class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    md5 = Column(String, nullable=False, unique=True)
    content = Column(LargeBinary, nullable=False)

Base.metadata.create_all(engine)

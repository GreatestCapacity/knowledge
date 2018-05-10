from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtCore import QUrl
from markdown import markdown
from lib.database import engine
from lib.data_access import DataAccess
import os


class MarkdownView(QWebView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.data_access = DataAccess(engine)

        self.load(QUrl.fromLocalFile(os.getcwd() + '/desktop_mode/index.html'))

    def show_default_page(self):
        self.load(QUrl.fromLocalFile(os.getcwd() + '/desktop_mode/index.html'))

    def show_note(self, note_content):
        html_content = markdown(note_content,
                        extensions=['markdown.extensions.extra',
                                    'markdown.extensions.codehilite',
                                    'markdown.extensions.toc',
                                    'markdown.extensions.tables'])

        container = self.page().currentFrame().findFirstElement('div.container')
        container.setInnerXml(html_content)
        for table in container.findAll('table'):
            table.addClass('table')
        self.page().currentFrame().evaluateJavaScript('renderMathInElement(document.body);')

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QLineEdit
)
from PyQt5.QtCore import QThread, pyqtSignal, QFile, QTextStream

import look_here


"""
I take no pride in this UI
its quick and dirty and a bit of a mess quite frankly
"""


TITLE = "Viewer: \n"


class StreamWorker(QThread):
    """
    A worker thread to handle the streaming of content from a generator function.
    """


    new_content = pyqtSignal(str)

    def __init__(self, generator_func, input_string):
        super().__init__()
        self.generator_func = generator_func
        self.input_string = input_string

    def run(self):
        """Run the generator and emit content as it is produced."""
        try:
            res = self.generator_func(self.input_string)
            for content in res:
                self.new_content.emit(content)
        except Exception as e:
            self.new_content.emit(str(e))


class MarkdownStreamingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Look Here")
        self.resize(1600, 800)
        self.setStyleSheet("background-color: #2C2C2C; color: white;")  # Dark grayish-black with white text


        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Markdown viewer
        self.text_viewer = QTextEdit(self)
        self.text_viewer.setReadOnly(True)  # Make it read-only for viewing
        self.text_viewer.setAcceptRichText(True)  # Plain text for Markdown rendering
        self.apply_stylesheet("./ui/resource/styles.qss")
        self.text_viewer.setStyleSheet("font-size: 20px;")
        self.layout.addWidget(self.text_viewer)

        # User input for sending content
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("Ask something about this screenshot...")
        self.layout.addWidget(self.input_box)

        # Button to trigger streaming
        self.start_stream_button = QPushButton("Generate", self)
        self.start_stream_button.clicked.connect(self.start_streaming)
        self.input_box.returnPressed.connect(self.start_streaming)
        self.layout.addWidget(self.start_stream_button)

        # Markdown content buffer
        self.markdown_buffer = [TITLE]
        self.update_markdown()

        # Worker thread for streaming
        self.stream_worker = None

    def apply_stylesheet(self, filename):
        """Load and apply stylesheet from a file."""
        file = QFile(filename)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
            file.close()

    def start_streaming(self):
        """
        Start the generator-based streaming process.
        """
        self.clear_markdown()
        user_input = self.input_box.text()
        self.stream_worker = StreamWorker(look_here.process_image, user_input)
        self.stream_worker.new_content.connect(self.add_text)
        self.stream_worker.start()

    def add_text(self, text):
        """
        Add Markdown text dynamically to the viewer.
        :param text: Markdown-formatted string to add
        """
        self.markdown_buffer.append(text)
        self.update_markdown()

    def clear_markdown(self):
        self.markdown_buffer = [TITLE]
        self.update_markdown()

    def update_markdown(self):
        """Render the Markdown buffer into the text viewer."""
        self.text_viewer.setPlainText("".join(self.markdown_buffer))



def main():
    app = QApplication(sys.argv)
    window = MarkdownStreamingApp()
    window.show()
    sys.exit(app.exec_())


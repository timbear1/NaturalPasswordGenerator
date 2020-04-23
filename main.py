import sys, random, json, os.path
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout, \
    QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QGroupBox, QSpinBox, \
    QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.inputs = []

        self.setWindowIcon(QIcon(get_resource_path() + "icon.png"))
        self.setWindowTitle("Natural Password Generator v1.0.1")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.grid_layout = QGridLayout()
        central_widget.setLayout(self.grid_layout)

        self.create_buttons()
        self.create_input()
        self.create_output()

        self.grid_layout.setRowStretch(0, 0)
        self.grid_layout.setRowStretch(1, 0)
        self.grid_layout.setRowStretch(2, 1)
        self.grid_layout.setRowStretch(3, 1)
        self.grid_layout.setRowStretch(4, 1)

        if os.path.isfile("input.current"):
            self.restore()
        else:
            self.create_default()

    def closeEvent(self, _):
        self.save()

    def create_buttons(self):
        generate_password_btn = QPushButton("Generate Password", self)
        help_btn = QPushButton("Help && Tips", self)
        clear_output_btn = QPushButton("Clear Output", self)
        add_words_btn = QPushButton("Add Words Field", self)
        add_digits_btn = QPushButton("Add Digit(s) Field", self)
        add_characters_btn = QPushButton("Add Character(s) Field", self)

        generate_password_btn.clicked.connect(self.generate_password)
        help_btn.clicked.connect(self.help)
        clear_output_btn.clicked.connect(self.clear_output)
        add_words_btn.clicked.connect(self.create_words_field)
        add_digits_btn.clicked.connect(self.create_digits_field)
        add_characters_btn.clicked.connect(self.create_characters_field)

        self.grid_layout.addWidget(generate_password_btn, 0, 0, QtCore.Qt.AlignTop)
        self.grid_layout.addWidget(help_btn, 0, 1, QtCore.Qt.AlignTop)
        self.grid_layout.addWidget(clear_output_btn, 0, 2, QtCore.Qt.AlignTop)
        self.grid_layout.addWidget(add_words_btn, 1, 0, QtCore.Qt.AlignTop)
        self.grid_layout.addWidget(add_digits_btn, 1, 1, QtCore.Qt.AlignTop)
        self.grid_layout.addWidget(add_characters_btn, 1, 2, QtCore.Qt.AlignTop)

    def create_output(self):
        group = QGroupBox("Output:", self)
        layout = QVBoxLayout()
        group.setLayout(layout)
        group.setMinimumWidth(200)
        self.output = QTextEdit(self)
        layout.addWidget(self.output)
        self.grid_layout.addWidget(group, 0, 3, 8, 1)

    def create_input(self):
        widget = QWidget(self)
        self.input_widget = QHBoxLayout()
        self.input_widget.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(self.input_widget)
        self.grid_layout.addWidget(widget, 2, 0, 6, 3)

    @pyqtSlot()
    def create_words_field(self):
        self.inputs.append(WordInput(self.input_widget))
        self.add_input_remove_btn()

    @pyqtSlot()
    def create_digits_field(self):
        self.inputs.append(DigitsInput(self.input_widget))
        self.add_input_remove_btn()

    @pyqtSlot()
    def create_characters_field(self):
        self.inputs.append(CharactersInput(self.input_widget))
        self.add_input_remove_btn()

    def add_input_remove_btn(self):
        remove_btn = QPushButton("Remove")
        input_field = self.inputs[-1]
        remove_btn.clicked.connect(lambda: self.remove_input(input_field))
        self.inputs[-1].layout().addWidget(remove_btn, QtCore.Qt.AlignBottom)

    @pyqtSlot()
    def remove_input(self, input_field):
        self.inputs.remove(input_field)
        input_field.deleteLater()

    @pyqtSlot()
    def generate_password(self):
        password = ""
        for i in self.inputs:
            password += i.generate()
        self.output.append(password)
        self.output.repaint()

    @pyqtSlot()
    def clear_output(self):
        self.output.clear()
        self.output.repaint()

    @pyqtSlot()
    def help(self):
        msg_box = QMessageBox()
        msg_box.setMinimumSize(500, 1000)
        msg_box.setWindowTitle("Natural Password Generator")
        msg_box.setText("<h2>Help & Tips</h2>")
        msg_box.setInformativeText(
            """
                <h3>Inputs:</h3>
                <h5>Words input</h5>
                Add one word per line. When generating a password - a random line from each field is selected.<br/>
                <h5>Digits input</h5>
                Set the number of digits to generate. 1 digit is 0 to 9.<br/>
                <h5>Character input</h5>
                Set the number of special characters ['!', '#', '*', '&', '%'] to generate.<br/>
                <h3>Save state</h3>
                The current input configuration is saved to a file when closing the application.<br/>
                The file 'input.current' is saved next to the executable. To clear the save state just delete that file.<br/>
                <h3>Tips</h3>
                To make a more memorable password it's suggested to make all but the last word field adjectives (Pink, Big, Small).
                The last word field should then be nouns (House, Apple, Shoe). So the password ends up being something along the lines of; BigHouse or SmallPinkShoe.<br/>
                <br/>
                Words should also be capitalized to increase security.<br/>
                <h3>Contact</h3>
                Please report issues at:
                <a href=\"https://github.com/timotii48/NaturalPasswordGenerator/issues\">Github/Issues</a><br/>
                For new releases check:
                <a href=\"https://github.com/timotii48/NaturalPasswordGenerator/releases\">Github/Releases</a><br/>
                For anything else email me at: <a href=\"t.jungvig@hotmail.com\">t.jungvig@hotmail.com</a>
            """
            )
        msg_box.setTextFormat(QtCore.Qt.RichText)
        msg_box.setStandardButtons(QMessageBox.Close)
        msg_box.setDefaultButton(QMessageBox.Close)
        msg_box.exec()

    def save(self):
        data = {}
        data['inputs'] = []
        for i in self.inputs:
            data['inputs'].append(i.serialize())
        with open(get_save_path() + 'input.current', 'w') as outfile:
            json.dump(data, outfile, sort_keys=False, indent=4, separators=(',', ': '))

    def restore(self):
        with open('input.current') as json_file:
            data = json.load(json_file)
            for i in data['inputs']:
                if i['type'] == "words":
                    self.create_words_field()
                elif i['type'] == "digits":
                    self.create_digits_field()
                elif i['type'] == "characters":
                    self.create_characters_field()
                self.inputs[-1].deserialize(i)

    def create_default(self):
        self.create_words_field()
        self.create_words_field()
        self.create_digits_field()
        self.create_characters_field()


class WordInput(QGroupBox):
    def __init__(self, parent):
        QGroupBox.__init__(self, "Words")
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setFixedWidth(200)

        self.words_field = QTextEdit()
        layout.addWidget(self.words_field)

        parent.addWidget(self, QtCore.Qt.AlignTop)

    def clean_up(self):
        pass

    def generate(self):
        texts = self.words_field.toPlainText().splitlines()
        texts = [text.strip() for text in texts] # remove whitespace
        texts = [text for text in texts if text] # remove empty

        if len(texts) == 0:
            return ""

        return random.choice(texts)

    def serialize(self):
        return {
            'type': 'words',
            'input': self.words_field.toPlainText()
        }

    def deserialize(self, data):
        self.words_field.setPlainText(data['input'])


class DigitsInput(QGroupBox):
    def __init__(self, parent):
        QGroupBox.__init__(self, "Digit(s)")
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setFixedWidth(200)

        num_label = QLabel("Number of digits:")
        layout.addWidget(num_label, QtCore.Qt.AlignBottom)

        self.spin = QSpinBox()
        self.spin.setRange(1, 100)
        layout.addWidget(self.spin, QtCore.Qt.AlignTop)
        layout.addStretch(2000)

        parent.addWidget(self, QtCore.Qt.AlignTop)

    def clean_up(self):
        pass

    def generate(self):
        text = ""
        num = self.spin.value()
        for _ in range(num):
            text += str(random.randint(0, 9))
        return text

    def serialize(self):
        return {
            'type': 'digits',
            'input': self.spin.value()
        }

    def deserialize(self, data):
        self.spin.setValue(data['input'])


class CharactersInput(QGroupBox):
    def __init__(self, parent):
        QGroupBox.__init__(self, "Character(s)")
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setFixedWidth(200)

        num_label = QLabel("Number of characters:")
        layout.addWidget(num_label, QtCore.Qt.AlignBottom)

        self.spin = QSpinBox()
        self.spin.setRange(1, 100)
        layout.addWidget(self.spin, QtCore.Qt.AlignTop)
        layout.addStretch(2000)

        parent.addWidget(self, QtCore.Qt.AlignTop)

    def clean_up(self):
        pass

    def generate(self):
        chars = ['!', '#', '*', '&', '%']

        text = ""
        num = self.spin.value()
        for _ in range(num):
            text += random.choice(chars)

        return text

    def serialize(self):
        return {
            'type': 'characters',
            'input': self.spin.value()
        }

    def deserialize(self, data):
        self.spin.setValue(data['input'])


def get_resource_path():
    if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS + "/res/"
    else:
        return os.path.abspath(".") + "/"

def get_save_path():
    if hasattr(sys, 'frozen'):
        path = os.path.dirname(sys.executable)
        return path + "/"
    else:
        return ""

if __name__ == "__main__":
    APP = QtWidgets.QApplication(sys.argv)
    WIN = MainWindow()
    WIN.show()
    sys.exit(APP.exec_())

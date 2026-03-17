import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        # Creating the widgets
        self.label = QLabel("Enter city name:")
        self.input = QLineEdit()
        self.button = QPushButton("Get Weather")
        self.result = QLabel("")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.button)
        layout.addWidget(self.result)

        self.setLayout(layout)
        self.setWindowTitle("Simple Weather App")

        # cilcking the button
        self.button.clicked.connect(self.get_weather)

    def get_weather(self):
        city = self.input.text()

        api_key = "your api id"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        response = requests.get(url)
        data = response.json()

        # temperature
        temp_k = data["main"]["temp"]
        temp_c = temp_k - 273.15

        # result
        self.result.setText(f"{city}: {temp_c:.1f}°C")


# Running  the app
app = QApplication(sys.argv)
window = WeatherApp()
window.show()
sys.exit(app.exec_())
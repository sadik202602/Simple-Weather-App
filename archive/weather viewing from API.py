import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie


class WeatherApp(QWidget):

    def __init__(self):
        super().__init__()

        # Widgets
        self.city_label = QLabel("Enter City Name")
        self.city_input = QLineEdit()

        self.button = QPushButton("Get Weather")

        self.city_result = QLabel("")
        self.temp_label = QLabel("")
        self.gif_label = QLabel("")

        # Layout
        layout = QVBoxLayout()

        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.button)
        layout.addWidget(self.city_result)
        layout.addWidget(self.temp_label)
        layout.addWidget(self.gif_label)

        self.setLayout(layout)

        # Window settings
        self.setWindowTitle("SADIK's Weather App")

        # Alignment
        self.city_result.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.gif_label.setAlignment(Qt.AlignCenter)

        # Style
        self.setStyleSheet("""

        QLabel{
            font-family: Arial;
        }

        QLineEdit{
            font-size:25px;
        }

        QPushButton{
            font-size:20px;
            font-weight:bold;
        }

        """)

        # Button click
        self.button.clicked.connect(self.get_weather)

    def get_weather(self):

        city = self.city_input.text()

        api_key = "add your api here"

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            temp_k = data["main"]["temp"]
            temp_c = temp_k - 273.15

            # City name BIG
            self.city_result.setText(f"<b>{city}</b>")
            self.city_result.setStyleSheet("font-size:40px")

            # Temperature
            self.temp_label.setText(f"{temp_c:.1f} °C")
            self.temp_label.setStyleSheet("font-size:35px")

            # Show GIF
            self.show_weather_gif(temp_c)

        except requests.exceptions.HTTPError:

            if response.status_code == 404:
                self.temp_label.setText("City not found")

            else:
                self.temp_label.setText("API Error")

        except requests.exceptions.ConnectionError:

            self.temp_label.setText("No Internet Connection")

        except Exception:

            self.temp_label.setText("Something went wrong")

    def show_weather_gif(self, temp):

        if -15 <= temp < -10:
            gif = "very _very_cold_cat.gif"
    
        elif -10 <= temp < 0:
            gif = "freezing_cat_snow.gif"
    
        elif 0 <= temp < 10:
            gif = "cat_cold.gif"
    
        elif 10 <= temp < 20:
            gif = "cool_weather cat.gif"
    
        elif 20 <= temp < 30:
            gif = "warm_cat.gif"
    
        elif 30 <= temp < 40:
            gif = "hot cat.gif"
    
        else:
            gif = "very _very_cold_cat.gif"
    
        movie = QMovie(gif)
        self.gif_label.setMovie(movie)
        movie.start()


# Run App
app = QApplication(sys.argv)
window = WeatherApp()
window.show()
sys.exit(app.exec_())
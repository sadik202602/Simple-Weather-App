import sys
import requests
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie, QPixmap, QPainter, QColor, QBitmap, QBrush

def get_theme_name(weather_id, sunrise, sunset):
    # datetime.now().timestamp() = current time as a big number
    # (seconds counted from Jan 1, 1970 — called Unix time)
    now = datetime.now().timestamp()

    # True if current time is between sunrise and sunset
    is_day = sunrise < now < sunset

    if weather_id == 800 and not is_day:
        return "night_clear"
    elif weather_id == 800:
        return "sunny"
    elif 801 <= weather_id <= 804:
        return "cloudy"
    elif 500 <= weather_id <= 531:
        return "rainy"
    elif 200 <= weather_id <= 232:
        return "stormy"
    elif 600 <= weather_id <= 622:
        return "snowy"
    elif 700 <= weather_id <= 781:
        return "foggy"
    elif weather_id in (771, 781):
        return "windy"
    else:
        return "sunny" 
    
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
        self._bg_pixmap = None

        # Alignment
        self.city_result.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.gif_label.setStyleSheet("""
                                     QLabel {
                                         border-radius: 45px;
                                         background-color: rgba(0, 0, 0, 60);
                                         }
                                     """)

        # Style
        self.setStyleSheet("""
        QLabel {
            font-family: Arial;
            color: white;
            background: transparent;
        }
        QLineEdit {
            font-size: 20px;
            color: white;
            background: rgba(255, 255, 255, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.4);
            border-radius: 10px;
            padding: 6px;
        }
        QPushButton {
            font-size: 18px;
            font-weight: bold;
            color: white;
            background: rgba(255, 255, 255, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.4);
            border-radius: 10px;
            padding: 8px;
        }
        QPushButton:hover {
            background: rgba(255, 255, 255, 0.30);
        }
        """)

        # Button click
        self.button.clicked.connect(self.get_weather)
        
    def paintEvent(self, event):
        painter = QPainter(self)

        if self._bg_pixmap and not self._bg_pixmap.isNull():
        # Scale the image to fill the whole window
        # Qt.KeepAspectRatioByExpanding = zoom in enough to cover
        # the full window even if we crop the edges slightly
        # Qt.SmoothTransformation = use smooth resizing, not pixelated
            scaled = self._bg_pixmap.scaled(self.size(), 
                                        Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, scaled)

        # Draw a dark transparent layer on top so text is readable
        # QColor(r, g, b, alpha) — alpha goes from 0 (invisible) to 255 (solid)
        # 140 = about 55% dark, enough to read white text but still see the photo
            painter.fillRect(self.rect(), QColor(0, 0, 0, 140))

        else:
            # No image yet — fill with plain dark color as placeholder
            painter.fillRect(self.rect(), QColor(30, 30, 50))

        painter.end()
        
    def load_background(self, theme_name):
    # Build the file path using an f-string
    # e.g. theme_name="rainy" → path="backgrounds/rainy.jpg"
        path = f"backgrounds/{theme_name}.jpg"

        pixmap = QPixmap(path)   # try to load the file

        if pixmap.isNull():
            # isNull() is True when the file wasn't found
            # or the file is corrupted / wrong format
            # Instead of crashing, we just skip the image
            self._bg_pixmap = None
            print(f"WARNING: Could not load {path}")
            # print() shows a message in the Spyder console — helpful for debugging
        else:
            self._bg_pixmap = pixmap

            self.update()
            # update() tells Qt "please call paintEvent again"
            # so the new background gets drawn immediately
            

    def get_weather(self):

        city = self.city_input.text()

        api_key = "ADD YOUR API HERE TO SEE WEATHER"

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            temp_k = data["main"]["temp"]
            temp_c = temp_k - 273.15
            weather_id = data["weather"][0]["id"]
            condition = data["weather"][0]["main"]
            sunrise    = data["sys"]["sunrise"]
            sunset     = data["sys"]["sunset"]

            # City name BIG
            self.city_result.setText(f"<b>{city.upper()}</b>")
            self.city_result.setStyleSheet("font-size:40px")

            # Temperature
            self.temp_label.setText(
                f'<span style="font-size:15px; font-weight:normal;">{condition}</span>'
                f'<br>'
                f'<span style="font-size:52px; font-weight:bold;">{temp_c:.0f}°C</span>'
            )
            self.temp_label.setStyleSheet("color:white; background:transparent;")
            self.temp_label.setTextFormat(Qt.RichText)

            # Show GIF
            self.show_weather_gif(temp_c)
            theme_name = get_theme_name(weather_id, sunrise, sunset)
            self.load_background(theme_name)

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
            gif = "GIFs/very _very_cold_cat.gif"
    
        elif -10 <= temp < 0:
            gif = "GIFs/freezing_cat_snow.gif"
    
        elif 0 <= temp < 10:
            gif = "GIFs/cat_cold.gif"
    
        elif 10 <= temp < 20:
            gif = "GIFs/cool_weather cat.gif"
    
        elif 20 <= temp < 30:
            gif = "GIFs/warm_cat.gif"
    
        elif 30 <= temp < 40:
            gif = "GIFs/hot_cat.gif"
    
        else:
            gif = "GIFs/very _very_cold_cat.gif"
    
        movie = QMovie(gif)
        # Scale the GIF down to 90x90 pixels to fit in our circle
        movie.setScaledSize(movie.scaledSize().__class__(90, 90))
        self.gif_label.setMovie(movie)
        movie.start()
        
        # Make the label a fixed 90x90 square first
        self.gif_label.setFixedSize(90, 90)
        
        # Now create a circular mask (stencil)
        # QBitmap = a black and white image used as a cutout
        # Black pixels = hidden, White pixels = visible
        mask = QBitmap(90, 90)
        mask.fill(Qt.color0)          # fill everything BLACK = hide everything
        
        mask_painter = QPainter(mask)
        mask_painter.setBrush(Qt.color1)     # white = show
        mask_painter.setPen(Qt.NoPen)        # no border line
        mask_painter.drawEllipse(0, 0, 90, 90)  # draw white circle
        mask_painter.end()
        
        self.gif_label.setMask(mask)   # apply the stencil to the label


# Run App
app = QApplication(sys.argv)
window = WeatherApp()
window.show()
sys.exit(app.exec_())
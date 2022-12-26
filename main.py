import json
import requests
import schedule
import subprocess
import sys
import time as tm

from datetime import datetime
from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QFormLayout,
    QLineEdit,
    QWidget,
)

times = {
	"Fajr": dict(),
	"Dhuhr": dict(), 
	"Asr": dict(),
	"Maghrib": dict(),
	"Isha'a": dict(),
	"current_time": None
}

DB_NAME = "times_db.json"
CITY = "bordj ghdir"
API_URL = f"https://dailyprayer.abdulrcs.repl.co/api/{CITY}"

# Update times in db from https://dailyprayer.abdulrcs.repl.co/api
response = requests.get(API_URL)

if response.status_code == 200:
	with open(DB_NAME, "w") as db:
		db.write(json.dumps(response.json(), indent=4))
else:
	print("Warning: db not updated")

# Get time from db
times_in_db = json.load(open(DB_NAME, 'r'))

def sendmessage(message="Go to pray"):
	subprocess.Popen(['notify-send', message])
	return

def notify_user(data):
	sendmessage(f"Go to pray {time}")
	default_font = QFont()
	current_time_font = QFont()
	current_time_font.setBold(True)
	data["times"][data["times"]["current_time"]]["widget"].setFont(default_font)
	data["times"][data["time"]]["widget"].setFont(current_time_font)
	data["times"]["current_time"] = time
	

# Update times var
now = datetime.now()
for time in list(times.keys())[:-1]:
	value = times_in_db.get("today").get(time)
	times[time]["time"] = value
	hour, minute = times[time]["time"].split(":")
	times[time]["timestamp"] = datetime(now.year, now.month, now.day, int(hour), int(minute)).time()
	
	# Schedule Notification about Prayer time
	schedule.every().day.at(value).do(notify_user, {"time": time, "times": times})


keys = list(times.keys())
for (time1, time2) in zip(keys[:-2], keys[1:-1]):
	if times[time1]["timestamp"] <= now.time() < times[time2]["timestamp"]:
		times["current_time"] = time1
		break

if times["current_time"] is None:
	times["current_time"] = "Isha'a"

class SchudulerThread(QThread):
	def run(self, *args, **kwargs):
		while 1: 
			tm.sleep(40)
			schedule.run_pending()

scheduler = SchudulerThread()


def create_app():

	app = QApplication([])

	window = QWidget()

	window.setWindowTitle("Prayer Times")


	layout = QFormLayout()
	
	current_time_font = QFont()
	current_time_font.setBold(True)

	for time, data in list(times.items())[:-1]:	
		widget = QLineEdit()
		widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
		widget.setText(data['time'])
		widget.setReadOnly(True)
		data['widget'] = widget	
		layout.addRow(time, widget)
		
	times[times["current_time"]]["widget"].setFont(current_time_font)

	window.setLayout(layout)


	window.show()
	
	scheduler.start()

	sys.exit(app.exec())

if __name__ == "__main__":
	create_app()
	


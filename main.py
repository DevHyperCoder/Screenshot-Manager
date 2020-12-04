from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import glob
import shutil
from os.path import expanduser
import sys

# Constants
PICTURES_DIR = expanduser("~") + '/Pictures'
SCREENSHOT_DIR = expanduser("~") + "/Screenshots/"
SCREENSHOT_FILE = "Screenshot*"


class CustomHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Wait for a while so that the file can be written to disk
        time.sleep(1)
        print(event)
        move_files()


def main():
    print("Starting Screenshot manager")

    try:
        observe = sys.argv[1]
    except IndexError:
        observe = "y"

    if observe == "n":
        print("Moving all Screenshot* files")
        move_files()
        return

    # Initiate a observer
    observer = Observer()
    event_handler = CustomHandler()
    observer.schedule(event_handler, PICTURES_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
    print("Stopping Screenshot manager")


def move_files():
    for file in glob.glob(PICTURES_DIR + "/" + SCREENSHOT_FILE):
        print(file)
        shutil.move(file, SCREENSHOT_DIR)


if __name__ == '__main__':
    main()

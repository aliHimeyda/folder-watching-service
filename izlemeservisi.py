import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# JSON log dosyası
log_file = "/home/ubuntu/bsm/logs/changes.json"

class Watcher:
    DIRECTORY_TO_WATCH = "/home/ubuntu/bsm/test"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def process(event):
        data = {
            "event_type": event.event_type,
            "src_path": event.src_path,
            "is_directory": event.is_directory
        }
        with open(log_file, "a") as log:
            log.write(json.dumps(data) + "\n")

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)

if __name__ == "__main__":
    watcher = Watcher()
    watcher.run()

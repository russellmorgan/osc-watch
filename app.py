from flask import Flask, request, jsonify, render_template, Response
from pythonosc.udp_client import SimpleUDPClient
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import threading
import os
from datetime import datetime

app = Flask(__name__)

client = None
observer = None
watch_thread = None

log_messages = []  # Global log list

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"Created event detected: {event}")  # Debug print
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            osc_message = [filename, timestamp]
            log_entry = f"OSC (created): /newfile {osc_message}"
            log_messages.append(log_entry)
            print(f"Sending OSC (created): {osc_message}")  # Debug print
            client.send_message("/newfile", osc_message)
            # Add test message log format for consistency with send_test
            log_messages.append(f"Message sent: /newfile {osc_message}")

    def on_moved(self, event):
        print(f"Moved event detected: {event}")  # Debug print
        if not event.is_directory:
            filename = os.path.basename(event.dest_path)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            osc_message = [filename, timestamp]
            log_entry = f"OSC (moved): /newfile {osc_message}"
            log_messages.append(log_entry)
            print(f"Sending OSC (moved): {osc_message}")  # Debug print
            client.send_message("/newfile", osc_message)
            log_messages.append(f"Message sent: /newfile {osc_message}")

@app.route('/')
def index():
    return render_template('index.html')

# Set this variable to the directory you want to use for testing
TEST_DIRECTORY = r""  # Change this path as needed

@app.route('/start', methods=['POST'])
def start_monitoring():
    print("Starting monitoring...")  # Debug print
    global client, observer, watch_thread
    data = request.get_json()
    # Use the test directory if specified, otherwise use the one from the request
    directory = TEST_DIRECTORY if TEST_DIRECTORY else data['directory']
    ip = data['ip']
    port = int(data['port'])

    client = SimpleUDPClient(ip, port)

    if observer:
        observer.stop()
        observer.join()

    observer = Observer()
    observer.schedule(NewFileHandler(), path=directory, recursive=False)
    observer.start()

    return jsonify({"status": "Monitoring started for directory: " + directory})

@app.route('/stop', methods=['POST'])
def stop_monitoring():
    global observer
    if observer:
        observer.stop()
        observer.join()
        observer = None
    return jsonify({"status": "Monitoring stopped."})

@app.route('/send_test', methods=['POST'])
def send_test():
    data = request.get_json()
    ip = data['ip']
    port = int(data['port'])
    test_client = SimpleUDPClient(ip, port)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    osc_message = ["test file", timestamp]
    test_client.send_message("/newfile", osc_message)
    return jsonify({
        "status": f"Test message sent: /newfile {osc_message}"
    })

@app.route('/log', methods=['GET'])
def get_log():
    return jsonify({"log": log_messages})

@app.route('/clear_log', methods=['POST'])
def clear_log():
    log_messages.clear()
    return jsonify({"status": "Log cleared."})

@app.route('/stream')
def stream():
    def event_stream():
        last_len = 0
        while True:
            if len(log_messages) > last_len:
                # Send only new log entries
                for entry in log_messages[last_len:]:
                    yield f"data: {entry}\n\n"
                last_len = len(log_messages)
            time.sleep(1)
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True)

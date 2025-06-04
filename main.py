import tkinter as tk
from app import TELCJsonApp
import keyboard
import atexit
from flask import Flask, request, jsonify
import threading
import queue

app_flask = Flask(__name__)
data_queue = queue.Queue()

@app_flask.route('/api/insert', methods=['POST'])
def insert_data():
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' in JSON"}), 400
        data_queue.put(data['text'])
        return jsonify({"status": "Text queued for insertion"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_flask():
    app_flask.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def cleanup():
    try:
        keyboard.unhook_all()
        print("Cleaned up keyboard hooks")
    except Exception as e:
        print(f"Error cleaning up: {str(e)}")

atexit.register(cleanup)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    root = tk.Tk()
    app = TELCJsonApp(root, data_queue)
    root.mainloop()

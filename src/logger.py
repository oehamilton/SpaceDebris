
# logger.py
# src/logger.py
# Creating a simple Flask logger service to write logs to a database maybe PostgreSQL or a file
# or any other storage solution. This service will be used by the main application to log messages

from flask import Flask, request, jsonify
from flask_cors import CORS
import io
import threading
import time
import os
import traceback
from pathlib import Path

logger = Flask(__name__)
CORS(logger)

SCRIPT_DIR = Path(__file__).parent
LOG_PATH = SCRIPT_DIR.parent / "logs" / "startup.log"


@logger.route('/log', methods=['POST','GET'])
def log():
    try:
        if request.method == 'GET':
            # Handle GET requests with query parameters
            app_name = request.args.get('app_name')
            subject = request.args.get('subject')
            message = request.args.get('message')
            if not app_name:
                return jsonify({"error": "App Name Required"}), 400
            if not subject:
                return jsonify({"error": "Log Subject Required"}), 400
            if not message:
                return jsonify({"error": "Log Message Required"}), 400
        else:
            if 'subject' not in request.json:
                return jsonify({"error": "Log Subject Required"}), 400
            if 'message' not in request.json:
                return jsonify({"error": "Log Message Required"}), 400 
            if 'app_name' not in request.json:
                return jsonify({"error": "App Name Required"}), 400
            app_name = request.json['app_name']
            subject = request.json['subject']
            message = request.json['message']

       
        log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {app_name} - {subject}: {message}\n"
        with open(LOG_PATH, 'a') as log_file:
            log_file.write(log_entry)


        return jsonify({
            "Subject": subject,
            "log_entry": log_entry.strip()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))  # Use $PORT or default to 5001
    logger.run(host='0.0.0.0', port=port, debug=True)
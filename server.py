import hashlib
import threading
from flask import Flask, request, redirect, jsonify
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# URL Storage (In-memory for simplicity)
url_store = {}
short_to_long = {}
lock = threading.Lock()

# Helper Function: Generate Short URL
def shorten_url(long_url):
    """Generates a unique short URL based on a hash of the long URL."""
    hash_object = hashlib.sha256(long_url.encode())
    short_url = hash_object.hexdigest()[:8]  # Use first 8 characters for brevity
    return short_url

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.json
    long_url = data.get('url')
    if not long_url:
        logging.info("Invalid URL provided")
        return jsonify({'error': 'Invalid URL provided'}), 400

    with lock:
        if long_url in url_store:
            short_url = url_store[long_url]
        else:
            short_url = shorten_url(long_url)
            url_store[long_url] = short_url
            short_to_long[short_url] = long_url

    logging.info(f"Shortened URL: {long_url} -> {short_url}")
    return jsonify({'short_url': short_url}), 201

@app.route('/retrieve/<short_url>', methods=['GET'])
def retrieve(short_url):
    with lock:
        long_url = short_to_long.get(short_url)

    if not long_url:
        logging.info(f"Short URL not found: {short_url}")
        return jsonify({'error': 'Short URL not found'}), 404

    logging.info(f"Retrieved URL: {short_url} -> {long_url}")
    return jsonify({'long_url': long_url}), 200

@app.route('/<short_url>', methods=['GET'])
def redirect_to_url(short_url):
    with lock:
        long_url = short_to_long.get(short_url)

    if not long_url:
        logging.info(f"Short URL not found for redirection: {short_url}")
        return jsonify({'error': 'Short URL not found'}), 404

    logging.info(f"Redirecting to: {long_url} from {short_url}")
    return redirect(long_url, code=302)
#I let the status as 301 (temporary redirect) because the server is not running on a real domain


if __name__ == '__main__':
    app.run(debug=True)

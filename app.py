from flask import Flask, request, jsonify
from functools import wraps
import com.token as token
import tracking.daehan as daehan

app = Flask(__name__)

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token_id = request.form.get("token")
        if not token_id:
            return jsonify({"error": "Token is missing"}), 401

        client_key = token.verify_token(token_id)
        if client_key is None:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_function

@app.route("/create_token", methods=["POST"])
def create_token_route():
    client_key = request.form.get("client_key")
    token_id = token.create_token(client_key)

    if token_id is None:
        return jsonify({"error": "Invalid client key"}), 401

    return jsonify({"token": token_id})

@app.route("/track", methods=["POST"])
@token_required
def track_parcel():
    tracking_number = request.form.get("tracking_number")

    tracking_result = daehan.get_daehan_tracking_info(tracking_number)

    if tracking_result is None:
        return jsonify({"error": "Invalid tracking number"}), 400

    return jsonify(tracking_result)

if __name__ == "__main__":
    app.run()

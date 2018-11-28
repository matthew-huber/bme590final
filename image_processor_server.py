from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/download", methods=["GET"])
def server_gui(processed_data):

    return


@app.route("/upload", methods=['POST'])
def gui_server():
    r = request.get_json()

    return


if __name__ == "__main__":
    app.run(host="0.0.0.0")

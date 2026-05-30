from flask import Flask, request, jsonify, send_from_directory
from executor.kernel import handle
from executor.control_center import CONTROL_CENTER_HTML
from executor.security import check_token

app = Flask(__name__)

@app.route("/")
def home():
    return CONTROL_CENTER_HTML

@app.route("/chat", methods=["POST"])
def chat():
    if not check_token(request):
        return jsonify({"error": "unauthorized"}), 401
    data = request.get_json()
    cmd = data.get("command", "")
    return jsonify(handle(cmd, {}))

from executor.health import backup as create_backup
from executor.health import status as health_status

@app.route("/health")
def health():
    return jsonify(health_status())

@app.route("/backup")
def backup_route():
    return jsonify(create_backup())

from executor.file_reader import save_upload, read_text

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f:
        return jsonify({"error": "no_file"})
    return jsonify(save_upload(f))

@app.route("/read-file", methods=["POST"])
def read_file_route():
    data = request.get_json()
    path = data.get("path", "")
    return jsonify({"content": read_text(path)})


from executor.image_reader import save_image, image_preview

@app.route("/upload-image", methods=["POST"])
def upload_image():
    f = request.files.get("file")
    if not f:
        return jsonify({"error": "no_image"})
    return jsonify(save_image(f))

@app.route("/image-preview", methods=["POST"])
def image_preview_route():
    data = request.get_json()
    path = data.get("path", "")
    return jsonify(image_preview(path))


from executor.android_sense import sense as android_sense

@app.route("/sense")
def sense_route():
    return jsonify(android_sense())


from executor.app_builder import list_apps

@app.route("/apps")
def apps_list():
    return jsonify(list_apps())

@app.route("/apps/<name>/")
def open_generated_app(name):
    return send_from_directory(f"generated_apps/{name}", "index.html")

if __name__ == "__main__":
    print("🧠 NUS AI OS LEVEL 22 RUNNING")
    app.run(host="0.0.0.0", port=5000)

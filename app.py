from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(service="DevSecOps Security Pipeline Demo", endpoints=["/health", "/hello?name=Developer"])


@app.get("/health")
def health():
    return jsonify(status="ok"), 200


@app.get("/hello")
def hello():
    name = request.args.get("name", "Developer").strip() or "Developer"
    return jsonify(message=f"Hello, {name}!"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

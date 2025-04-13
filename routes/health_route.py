from flask import jsonify

def init_health_route(app):
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"status": "ok", "service": "bookmark_service"})
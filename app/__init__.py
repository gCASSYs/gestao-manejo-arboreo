import os

from flask import Flask

from .db import init_app


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-only-change-me"),
        DATABASE=os.path.join(app.instance_path, "manejo.db"),
    )

    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)
    init_app(app)

    from .routes import bp

    app.register_blueprint(bp)

    @app.after_request
    def adicionar_cabecalhos_seguranca(response):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self' https://cdn.jsdelivr.net; "
            "script-src 'none'; img-src 'self' data:"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        return response

    return app

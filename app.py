"""
Chalice entry point for yonah-agent (framework upstream).

This module registers the role-gated blueprints + the WebSocket handler.
The conversational agent (Yonah) lives in agent/yonah/yonah_agent.py and is
invoked through the Blueprint route handlers.

Architecture reference: see README.md.
"""
from chalice import Chalice, CORSConfig

from chalicelib.blueprints.api_key_auth import api_key_auth_blueprint
from chalicelib.blueprints.artefact_api import artefact_blueprint
from chalicelib.blueprints.evaluation_api import evaluation_blueprint
from chalicelib.blueprints.account_api import account_blueprint
from chalicelib.blueprints.pipeline_ws import pipeline_ws_blueprint

app = Chalice(app_name="yonah-agent")
app.experimental_feature_flags.update({"WEBSOCKETS"})
app.websocket_api.session.configuration_table = None  # set per-stage via env

# Open CORS for the demo deployment; tighten before production.
_cors = CORSConfig(allow_origin="*", allow_headers=["Authorization", "Content-Type"])

# Register Blueprints — each one carries its own role gating
app.register_blueprint(api_key_auth_blueprint, url_prefix="/auth")
app.register_blueprint(artefact_blueprint, url_prefix="/artefact")
app.register_blueprint(evaluation_blueprint, url_prefix="/eval")
app.register_blueprint(account_blueprint, url_prefix="/account")
app.register_blueprint(pipeline_ws_blueprint)  # WSS routes register at root


@app.route("/", cors=_cors)
def index():
    """Health check + version stamp."""
    return {
        "service": "yonah-agent",
        "status": "ok",
        "agent": "Yonah",
        "tools": [
            "build_artefact",
            "publish_artefact",
            "commit_decision",
            "tutor_me",
            "submit_draft",
            "query_my_provenance",
            "delete_my_data",
        ],
    }

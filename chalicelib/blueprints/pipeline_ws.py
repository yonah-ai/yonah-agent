"""pipeline_ws: TODO — see DEPLOY.md and the framework paper §4 for the tool surface this blueprint exposes.

Live envelope-flow visualisation feed; subscribes the connected client to
the provenance-graph append stream filtered to envelopes the client is
authorised to see.
"""
from chalice import Blueprint

pipeline_ws_blueprint = Blueprint(__name__)


# TODO: register the route handlers for this blueprint.
# See agent/yonah/tools/ for the corresponding tool stubs.

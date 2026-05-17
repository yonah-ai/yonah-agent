"""artefact_api: TODO — see DEPLOY.md and the framework paper §4 for the tool surface this blueprint exposes.

Routes the build_artefact + publish_artefact tools (authority-audience side).
Vertical forks subclass the tool implementations; the route surface is
framework-canonical.
"""
from chalice import Blueprint

artefact_blueprint = Blueprint(__name__)


# TODO: register the route handlers for this blueprint.
# See agent/yonah/tools/ for the corresponding tool stubs.

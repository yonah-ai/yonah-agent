"""evaluation_api: TODO — see DEPLOY.md and the framework paper §4 for the tool surface this blueprint exposes.

Routes the submit_draft + commit_decision + query_my_provenance tools.
Vertical forks subclass the tool implementations; the route surface is
framework-canonical.
"""
from chalice import Blueprint

evaluation_blueprint = Blueprint(__name__)


# TODO: register the route handlers for this blueprint.
# See agent/yonah/tools/ for the corresponding tool stubs.

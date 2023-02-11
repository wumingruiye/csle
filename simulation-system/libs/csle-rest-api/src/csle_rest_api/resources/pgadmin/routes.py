"""
Routes and sub-resources for the /pgadmin resource
"""

from flask import Blueprint, jsonify, request
from csle_common.controllers.management_system_controller import ManagementSystemController
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
pgadmin_bp = Blueprint(api_constants.MGMT_WEBAPP.PGADMIN_RESOURCE, __name__,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.PGADMIN_RESOURCE}")


@pgadmin_bp.route("",
                  methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def pgadmin():
    """
    :return: static resources for the /pgadmin url
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    running = ManagementSystemController.is_pgadmin_running()
    port = constants.COMMANDS.PGADMIN_PORT
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        if running:
            ManagementSystemController.stop_pgadmin()
            running = False
        else:
            ManagementSystemController.start_pgadmin()
            running = True
    pgadmin_ip = "localhost"
    if constants.CONFIG_FILE.PARSED_CONFIG is not None:
        pgadmin_ip = constants.CONFIG_FILE.PARSED_CONFIG.metastore_ip
        port = constants.CONFIG_FILE.PARSED_CONFIG.pgadmin_port
    pgadmin_dict = {
        api_constants.MGMT_WEBAPP.RUNNING_PROPERTY: running,
        api_constants.MGMT_WEBAPP.PORT_PROPERTY: port,
        api_constants.MGMT_WEBAPP.URL_PROPERTY: f"http://{pgadmin_ip}:{port}/"
    }
    response = jsonify(pgadmin_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE

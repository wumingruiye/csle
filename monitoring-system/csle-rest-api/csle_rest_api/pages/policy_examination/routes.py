"""
Routes and resources for the /policy-examination-page page
"""

from flask import Blueprint
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants


# Creates a blueprint "sub application" of the main REST app
policy_examination_page_bp = Blueprint(api_constants.MGMT_WEBAPP.POLICY_EXAMINATION_PAGE_RESOURCE, __name__,
                                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                                  f"{api_constants.MGMT_WEBAPP.POLICY_EXAMINATION_PAGE_RESOURCE}",
                                       static_url_path=f'{constants.COMMANDS.SLASH_DELIM}'
                                               f'{api_constants.MGMT_WEBAPP.POLICY_EXAMINATION_PAGE_RESOURCE}'
                                               f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.STATIC}',
                                       static_folder='../../../csle-mgmt-webapp/build')


@policy_examination_page_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def policy_examination_page():
    """
    :return: static resources for the /policy-examination-page url
    """
    return policy_examination_page_bp.send_static_file(api_constants.MGMT_WEBAPP.STATIC_RESOURCE_INDEX)
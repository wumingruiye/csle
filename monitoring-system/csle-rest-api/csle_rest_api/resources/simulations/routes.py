"""
Routes and resources for the /simulations resource
"""
import base64
from flask import Blueprint, jsonify, request
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.simulation_env_manager import SimulationEnvManager

# Creates a blueprint "sub application" of the main REST app
simulations_bp = Blueprint(
    api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}")


@simulations_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def simulations():
    """
    The /simulations resource

    :return: Returns a list of simulations, a list of simulation ids, or deletes all simulations
    """
    # Check if ids query parameter is True, then only return the ids and not the whole dataset
    ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
    if ids is not None and ids:
        return simulation_ids()
    all_simulations = MetastoreFacade.list_simulations()
    all_images = MetastoreFacade.list_simulation_images()
    simulations_dicts= {}
    for sim in all_simulations:
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            for sim_name_img in all_images:
                sim_name, img = sim_name_img
                if sim_name == sim.name:
                    sim.image = base64.b64encode(img).decode()
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            SimulationEnvManager.uninstall_simulation(sim)

    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
        simulations_dicts = list(map(lambda x: x.to_dict(), all_simulations))
    elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        simulations_dicts = {}
    response = jsonify(simulations_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response


def simulation_ids():
    """
    :return: the list of simulation ids as an HTTP response
    """
    simulation_ids = MetastoreFacade.list_simulation_ids()
    response_dicts = []
    for tup in simulation_ids:
        response_dicts.append({
            "id": tup[0],
            "simulation": tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response


@simulations_bp.route('/<simulation_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                   api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def get_simulation(simulation_id: int):
    """
    The /simulations/id resource. Gets or delets a simulation with a given id.

    :param simulation_id: the id of the simulation
    :return: the simulation or deletes the simulation
    """
    simulation = MetastoreFacade.get_simulation(simulation_id)
    response = jsonify({})
    if simulation is not None:
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            response = jsonify(simulation.to_dict())
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            SimulationEnvManager.uninstall_simulation(simulation)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response

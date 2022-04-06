from typing import List, Union, Any, Tuple
import psycopg
import jsonpickle
import json
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_common.dao.emulation_config.emulation_simulation_trace import EmulationSimulationTrace
from csle_common.logging.log import Logger
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics


class MetastoreFacade:
    """
    Facade for the metastore, contains methods for querying the metastore
    """

    @staticmethod
    def list_emulations() -> List[EmulationEnvConfig]:
        """
        :return: A list of emulations in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATIONS_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_emulation_record_to_dto(x), records))
                return records

    @staticmethod
    def get_emulation(name: str) -> Union[None, EmulationEnvConfig]:
        """
        Function for extracting the metadata of an emulation with a given name

        :param name: the name of the emulation
        :return: The emulation config or None if the emulation was not found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATIONS_TABLE} WHERE name = %s", (name,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_emulation_record_to_dto(emulation_record=record)
                return record

    @staticmethod
    def _convert_emulation_record_to_dto(emulation_record) -> EmulationEnvConfig:
        """
        Converts an emulation record fetched from the metastore into a DTO

        :param emulation_record: the record to convert
        :return: the DTO representing the record
        """
        emulation_config_json_str = json.dumps(emulation_record[2], indent=4, sort_keys=True)
        emulation_env_config: EmulationEnvConfig = jsonpickle.decode(emulation_config_json_str)
        return emulation_env_config

    @staticmethod
    def _convert_emulation_trace_record_to_dto(emulation_trace_record) -> EmulationTrace:
        """
        Converts an emulation trace record fetched from the metastore into a DTO

        :param emulation_trace_record: the record to convert
        :return: the DTO representing the record
        """
        emulation_trace_json_str = json.dumps(emulation_trace_record[2], indent=4, sort_keys=True)
        emulation_trace: EmulationTrace = EmulationTrace.from_dict(json.loads(emulation_trace_json_str))
        return emulation_trace

    @staticmethod
    def _convert_emulation_simulationtrace_record_to_dto(emulation_simulation_trace_record) -> EmulationSimulationTrace:
        """
        Converts an emulation-simulkation trace record fetched from the metastore into a DTO

        :param emulation_simulation_trace_record: the record to convert
        :return: the DTO representing the record
        """
        emulation_simulation_trace_json_str = json.dumps(emulation_simulation_trace_record[2], indent=4,
                                                         sort_keys=True)
        emulation_simulation_trace: EmulationSimulationTrace = \
            EmulationSimulationTrace.from_dict(json.loads(emulation_simulation_trace_json_str))
        return emulation_simulation_trace

    @staticmethod
    def _convert_simulation_trace_record_to_dto(simulation_trace_record) -> SimulationTrace:
        """
        Converts an emulation trace record fetched from the metastore into a DTO

        :param simulation_trace_record: the record to convert
        :return: the DTO representing the record
        """
        simulation_trace_json_str = json.dumps(simulation_trace_record[2], indent=4, sort_keys=True)
        simulation_trace: SimulationTrace = SimulationTrace.from_dict(json.loads(simulation_trace_json_str))
        return simulation_trace

    @staticmethod
    def _convert_emulation_statistics_record_to_dto(emulation_statistics_record) -> EmulationStatistics:
        """
        Converts an emulation statistics record fetched from the metastore into a DTO

        :param emulation_statistics_record: the record to convert
        :return: the DTO representing the record
        """
        emulation_statistics_json_str = json.dumps(emulation_statistics_record[2], indent=4, sort_keys=True)
        emulation_statistics: EmulationStatistics = EmulationStatistics.from_dict(
            json.loads(emulation_statistics_json_str))
        return emulation_statistics

    @staticmethod
    def _convert_emulation_image_record_to_tuple(emulation_image_record) -> Tuple[str, bytes]:
        """
        Converts an emulation statistics record fetched from the metastore into a DTO

        :param emulation_image_record: the record to convert
        :return: a tuple (emulation name, image bytes)
        """
        emulation_name = emulation_image_record[1]
        image_bytes = emulation_image_record[2]
        return emulation_name, image_bytes

    @staticmethod
    def install_emulation(config: EmulationEnvConfig) -> Union[Any, int]:
        """
        Installs the emulation configuration in the metastore

        :param config: the config to install
        :return: id of the created row
        """
        Logger.__call__().get_logger().debug(f"Installing emulation:{config.name} in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                try:
                    config_json_str = json.dumps(json.loads(jsonpickle.encode(config)), indent=4, sort_keys=True)
                    cur.execute(f"INSERT INTO {constants.METADATA_STORE.EMULATIONS_TABLE} (name, config) "
                                f"VALUES (%s, %s) RETURNING id", (config.name, config_json_str))
                    id_of_new_row = cur.fetchone()[0]
                    conn.commit()
                    Logger.__call__().get_logger().debug(f"Emulation {config.name} installed successfully")
                    return id_of_new_row
                except psycopg.errors.UniqueViolation as e:
                    Logger.__call__().get_logger().debug(f"Emulation {config.name} is already installed")

    @staticmethod
    def uninstall_emulation(config: EmulationEnvConfig) -> None:
        """
        Uninstalls the emulation configuration in the metastore

        :param config: the config to uninstall
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Uninstalling emulation:{config.name} from the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.EMULATIONS_TABLE} WHERE name = %s", (config.name,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Emulation {config.name} uninstalled successfully")

    @staticmethod
    def save_emulation_trace(emulation_trace: EmulationTrace) -> Union[Any, int]:
        """
        Saves a trace from the emulation

        :param emulation_trace: the emulation trace to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Installing emulation trace for "
                                             f"emulation:{emulation_trace.emulation_name} in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(emulation_trace.to_dict(), indent=4, sort_keys=True)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.EMULATION_TRACES_TABLE} (emulation_name, trace) "
                            f"VALUES (%s, %s) RETURNING id", (emulation_trace.emulation_name, config_json_str))
                id_of_new_row = cur.fetchone()[0]
                conn.commit()
                Logger.__call__().get_logger().debug(f"Emulation trace for "
                                                     f"emulation {emulation_trace.emulation_name} saved successfully")
                return id_of_new_row

    @staticmethod
    def save_emulation_statistic(emulation_statistics: EmulationStatistics) -> Union[Any, int]:
        """
        Saves a DTO with emulation statistics to the metastore

        :param emulation_statistics: the emulation statistics to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Installing statistics "
                                             f"for emulation:{emulation_statistics.emulation_name} in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(emulation_statistics.to_dict(), indent=4, sort_keys=True)
                cur.execute(f"INSERT INTO "
                            f"{constants.METADATA_STORE.EMULATION_STATISTICS_TABLE} "
                            f"(emulation_name, statistics) "
                            f"VALUES (%s, %s) RETURNING id", (emulation_statistics.emulation_name, config_json_str))
                id_of_new_row = cur.fetchone()[0]
                conn.commit()
                Logger.__call__().get_logger().debug(f"Statistics for emulation "
                                                     f"{emulation_statistics.emulation_name} saved successfully")
                return id_of_new_row

    @staticmethod
    def list_emulation_statistics() -> List[EmulationStatistics]:
        """
        :return: A list of emulation statistics in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_STATISTICS_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_emulation_statistics_record_to_dto(x), records))
                return records

    @staticmethod
    def list_emulation_traces() -> List[EmulationTrace]:
        """
        :return: A list of emulation traces in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_TRACES_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_emulation_trace_record_to_dto(x), records))
                return records

    @staticmethod
    def list_simulation_traces() -> List[SimulationTrace]:
        """
        :return: A list of simulation traces in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SIMULATION_TRACES_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_simulation_trace_record_to_dto(x), records))
                return records

    @staticmethod
    def get_emulation_trace(id: int) -> Union[None, EmulationTrace]:
        """
        Function for fetching an emulation trace with a given id from the metastore

        :param id: the id of the emulation trace
        :return: The emulation trace or None if it could not be found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_TRACES_TABLE} WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_emulation_trace_record_to_dto(emulation_trace_record=record)
                return record

    @staticmethod
    def get_emulation_statistic(id: int) -> Union[None, EmulationStatistics]:
        """
        Function for fetching an emulation satistic with a given id from the metastore

        :param id: the id of the statistics
        :return: The emulation statistic or None if it could not be found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_STATISTICS_TABLE} "
                            f"WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_emulation_statistics_record_to_dto(
                        emulation_statistics_record=record)
                return record

    @staticmethod
    def get_simulation_trace(id: int) -> Union[None, SimulationTrace]:
        """
        Function for fetching a simulation trace with a given id from the metastore

        :param id: the id of the simulation trace
        :return: The simulation trace or None if it could not be found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SIMULATION_TRACES_TABLE} WHERE id = %d", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_simulation_trace_record_to_dto(simulation_trace_record=record)
                return record

    @staticmethod
    def save_simulation_trace(simulation_trace: SimulationTrace) -> Union[Any, int]:
        """
        Saves a trace from the simulation

        :param simulation_trace: the simulation trace to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Installing simulation trace "
                                             f"for simulation env:{simulation_trace.simulation_env} "
                                             f"in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(simulation_trace.to_dict(), indent=4, sort_keys=True)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.EMULATION_TRACES_TABLE} (gym_env, trace) "
                            f"VALUES (%s, %s) RETURNING id", (simulation_trace.simulation_env, config_json_str))
                id_of_new_row = cur.fetchone()[0]
                conn.commit()
                Logger.__call__().get_logger().debug(f"Simulation trace for "
                                                     f"env {simulation_trace.simulation_env} "
                                                     f"saved successfully")
                return id_of_new_row

    @staticmethod
    def save_emulation_simulation_trace(emulation_simulation_trace: EmulationSimulationTrace) -> None:
        """
        Saves an emulation_simulation trace

        :param emulation_simulation_trace: the emulation trace to save
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Installing emulation-simulation trace for "
                                             f"emulation:{emulation_simulation_trace.emulation_trace.emulation_name} "
                                             f"and simulation environment: "
                                             f"{emulation_simulation_trace.simulation_trace.simulation_env} in the "
                                             f"metastore")
        emulation_trace_id = MetastoreFacade.save_emulation_trace(
            emulation_trace=emulation_simulation_trace.emulation_trace)
        simulation_trace_id = MetastoreFacade.save_simulation_trace(
            simulation_trace=emulation_simulation_trace.simulation_trace)
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"INSERT INTO "
                            f"{constants.METADATA_STORE.EMULATION_SIMULATION_TRACES_TABLE} "
                            f"(emulation_trace, simulation_trace) "
                            f"VALUES (%d, %d) RETURNING id", (emulation_trace_id, simulation_trace_id))
                conn.commit()
                Logger.__call__().get_logger().debug(
                    f"Emulation-Simulation trace for "
                    f"emulation {emulation_simulation_trace.emulation_trace.emulation_name} "
                    f"and simulation: {emulation_simulation_trace.simulation_trace.simulation_env} saved successfully")

    @staticmethod
    def save_emulation_image(img: bytes, emulation_name: str) -> Union[Any, int]:
        """
        Saves the image of an emulation in the metastore

        :param img: the image data to save
        :param emulation_name: the name of the emulation
        :return: id of the created row
        """
        Logger.__call__().get_logger().debug(f"Saving image for emulation:{emulation_name} in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(f"INSERT INTO {constants.METADATA_STORE.EMULATION_IMAGES_TABLE} (emulation_name, image) "
                                f"VALUES (%s, %s) RETURNING id", (emulation_name, img))
                    id_of_new_row = cur.fetchone()[0]
                    conn.commit()
                    Logger.__call__().get_logger().debug(f"Saved image for emulation {emulation_name} successfully")
                    return id_of_new_row
                except Exception as e:
                    Logger.__call__().get_logger().warning(f"There was an error saving an image "
                                                         f"for emulation {emulation_name}")

    @staticmethod
    def list_emulation_images() -> List[Tuple[str, bytes]]:
        """
        :return: A list of emulation names and images in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_IMAGES_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_emulation_image_record_to_tuple(x), records))
                return records


    @staticmethod
    def get_emulation_img(emulation_name : str) -> Union[None, Tuple[str, bytes]]:
        """
        Function for fetching the image of a given emulation

        :param emulation_name: the name of the emulatin to fetch the image for
        :return: The simulation trace or None if it could not be found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_IMAGES_TABLE} "
                            f"WHERE emulation_name = %s", (emulation_name,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_emulation_image_record_to_tuple(emulation_image_record=record)
                return record
from pycr_common.util.experiments_util import util
from pycr_common.envs_model.config.generator.generator_util import GeneratorUtil

if __name__ == '__main__':
    containers_config = util.read_containers_config(util.default_containers_path())
    GeneratorUtil.upload_and_unzip_filesystem_cache(containers_config)

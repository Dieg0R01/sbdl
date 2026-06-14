import os
import sys

from lib import Utils
from lib.logger import Log4j


def _load_sbdl_env_file():
    env_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '.vscode', 'sbdl.env'
    )
    if not os.path.isfile(env_path):
        return
    with open(env_path, encoding='utf-8') as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, _, value = line.partition('=')
            key, value = key.strip(), value.strip()
            if key and key not in os.environ:
                os.environ[key] = value


if __name__ == '__main__':

    if len(sys.argv) >= 3:
        job_run_env = sys.argv[1].upper()
        load_date = sys.argv[2]
    else:
        _load_sbdl_env_file()
        if os.environ.get('SBDL_ENV') and os.environ.get('SBDL_LOAD_DATE'):
            job_run_env = os.environ['SBDL_ENV'].upper()
            load_date = os.environ['SBDL_LOAD_DATE']
        else:
            print("Usage: sbdl {local, qa, prod} {load_date} : Arguments are missing")
            print("  Or configure SBDL_ENV and SBDL_LOAD_DATE in .vscode/sbdl.env")
            sys.exit(-1)

    spark = Utils.get_spark_session(job_run_env)
    logger = Log4j(spark)

    logger.info("Finished creating Spark Session")

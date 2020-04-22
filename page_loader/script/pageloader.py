from page_loader import engine, cli
import sys
import logging
import os


class PageLoaderException(Exception):
    pass


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main():
    parser = cli.init_argparser()
    args = parser.parse_args()
    path = args.output
    path_log = os.path.join(path, 'Log_Page_Loader.log')
    url = args.url
    level = args.log
    logslevel = cli.qualifier(level)
    file_handler = logging.FileHandler(path_log)
    file_handler.setLevel(logslevel)
    formatter = logging.Formatter(
        '%(asctime)s  - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    formatter_console = logging.Formatter(
        '%(asctime)s - %(message)s')
    console.setFormatter(formatter_console)
    logger.addHandler(console)
    try:
        engine.get_page(path, url)
    except PageLoaderException:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

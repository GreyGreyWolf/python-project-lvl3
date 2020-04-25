from page_loader import engine, logger
import sys


def main():
    try:
        engine.start()
    except logger.PageLoaderException:
        sys.exit(1)


if __name__ == '__main__':
    main()

from page_loader import engine
import sys


def main():
    try:
        engine.start()
    except engine.PageLoaderException:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

import logging
import sys
from lib import utils
import os


def main():

    # set up for logging
    LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL,
              }
    if len(sys.argv) > 1:
        level_name = sys.argv[1]
        level = LEVELS.get(level_name, logging.NOTSET)
        logging.basicConfig(
            format='%(asctime)s - %(levelname)-8s - %(message)s\n',
            level=level,
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    logger = logging.getLogger()
    logger.debug('Entering main')

    output_file = 'new.html'

    num_pages_to_grab = 2
    logger.debug(f'Grabbing {num_pages_to_grab} pages.')

    try:
        os.remove(output_file)
    except OSError:
        pass

    utils.write_output('header.html')

    with open(output_file, 'a') as outfile:
        for page_number in range(num_pages_to_grab):
            html = utils.get_html_from_web(page_number)
            html_str = utils.get_artist_info_from_html(html)
            outfile.write(html_str)

    utils.write_output('footer.html')


if __name__ == '__main__':
    main()
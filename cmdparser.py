import sys
import os

from getopt import getopt
from fileio import FileIO
from mylogger import MyLoggger

logger = MyLoggger.initialize('MyFinance')


class ParseInput(object):
    input_file = '[None]'
    made_by = '[Default]'
    CONFIG = 'Production'
    opts = None
    arg = None

    def main(self, argv):
        try:
            opts, arg = getopt(argv, "hti:u:", ["help", "test", "input=", "user="])
        except getopt.GetoptError:
            self.usage()
            sys.exit(2)

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                logger.info('Detected switch" {}'.format(opt))
                self.usage()
                sys.exit(2)
            elif opt in ('-i', '--input'):
                logger.info('Detected switch" {}'.format(opt))
                self.input_file = arg
            elif opt in ('-u', '--user'):
                logger.info('Detected switch" {}'.format(opt))
                self.made_by = arg
            elif opt in ('-t', '--test'):
                logger.info('Detected switch" {}'.format(opt))
                self.CONFIG = 'Test'

        self.show_params()

        file_io = FileIO()
        file_io.read(self.input_file, self.made_by, self.CONFIG)

    def show_params(self):
        print('Input file is {}'.format(self.input_file))
        print('Expenses made by {}'.format(self.made_by))

    @staticmethod
    def usage():
        logger.info('System usage printed')
        os.system('clear')
        print('-i OR --input : input file to read from\n-u OR --user : Who created expenses \n')


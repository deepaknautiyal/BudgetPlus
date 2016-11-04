from databaseio import DatabaseIO
from mylogger import MyLoggger

logger = MyLoggger.initialize('MyFinance')


class FileIO(object):
    input_file = None
    config_file = None
    made_by = None
    CONFIG = None
    params = {}
    data = []
    keys = ['Date',
            'Type',
            'SubType',
            'TxnType',
            'PaymentType',
            'Merchant',
            'Category',
            'BankName',
            'AccountId',
            'AccountType',
            'Credit',
            'Debit',
            'Balance',
            'Outstanding',
            'AvailableLimit',
            'Notes',
            'Reimbursable',
            'Reimbursed'
            ]

    def read(self, file, user, config):
        self.input_file = file
        self.made_by = user
        self.CONFIG = config

        self.read_config(self.CONFIG)

        self.read_input()

    def read_config(self, config):
        if config == 'Test':
            self.config_file = 'config_test.txt'
        else:
            self.config_file = 'config_prod.txt'

        logger.info('Config file set to: {}'.format(self.config_file))

        with open(self.config_file, 'r') as file:
            for line in file:
                param_list = line.split('=')
                self.params[param_list.pop(0)] = param_list.pop(1)

    def read_input(self):
        with open(self.input_file, 'r') as file:
            for line in file:
                field_list = line.split(',')
                if field_list[0] == 'Date':
                    continue
                else:
                    self.data.append(dict(zip(self.keys, field_list)))

        logger.info('File read with {} values'.format(len(self.data)))

        db_io = DatabaseIO()
        DatabaseIO.initialize()
        logger.info('Database initialized')

        db_io.insert_expenses(self.data)
        logger.info('File successfully inserted to DB')

        db_io.transform(self.made_by)
        logger.info('New data transformed')



import datetime

from peewee import *
from mylogger import MyLoggger

db = SqliteDatabase('PersonalFinance.db')
logger = MyLoggger.initialize('MyFinance')


class BaseModel(Model):
    class Meta:
        database = db


class Expense(BaseModel):
    Date = DateTimeField(formats='%d/%m/%Y')  # Date
    Month = CharField(max_length=255, default='January')  # Month
    Week = IntegerField(default=0)  # Week of the year
    Type = CharField(max_length=255, default=None)  # Type
    SubType = CharField(max_length=255, default=None)  # SubType
    TxnType = CharField(max_length=255, default=None)  # TxnType
    PaymentType = CharField(max_length=255, default=None)  # Payment Type
    Merchant = CharField(max_length=255, default=None)  # Merchant/Receiver/Sender
    Category = CharField(max_length=255, default=None)  # Category
    UberCategory = CharField(max_length=255, default='Unknown')  # Uber Category
    Budgeted = CharField(max_length=255, default='NA')  # Budgeted (Y,N,NA)
    BankName = CharField(max_length=255, default=None)  # Bank Name
    AccountId = CharField(max_length=255, default=None)  # Account Id
    AccountType = CharField(max_length=255, default=None)  # Account Type
    Credit = FloatField(default=0.00)  # Credit
    Debit = FloatField(default=0.00)  # Debit
    Balance = FloatField(default=0.00)   # Balance
    Outstanding = FloatField(default=0.00)  # Outstanding
    AvailableLimit = FloatField(default=0.00)  # Available Limit
    Notes = TextField(default=None)  # Notes
    Reimbursable = BooleanField()  # Reimbursable
    Reimbursed = BooleanField()  # Reimbursed
    MadeBy = CharField(max_length=255, default='Unknown')    # made_by
    Transformed = CharField(max_length=255, default='No')    # Transformed (Y,N,NA)
    created_date = DateTimeField(default=datetime.datetime.now)  # date time when row was created


class DatabaseIO(object):
    @staticmethod
    def initialize():
        db.connect()
        logger.info('Database connected')

        db.create_tables([Expense], safe=True)
        logger.info('Table created')

    def insert_expenses(self, data):
        logger.info('insert_expenses')
        logger.info('Total rows in data structure: {}'.format(len(data)))

        with db.atomic():
            for idx in range(0, len(data), 35):
                Expense.insert_many(data[idx:idx+35]).execute()

        count = Expense.select().where(Expense.created_date.day==datetime.datetime.now().day).count()
        logger.info('Number of records inserted in DB: {}'.format(count))

    def transform(self, user):
        logger.info('Inside Transform')
        count = 0
        expenses = Expense.select().where(Expense.Transformed == 'No')

        logger.info('Number of records retrieved = {}'.format(len(expenses)))

        for expense in expenses:
            date_object = datetime.datetime.strptime(expense.Date, '%Y/%b/%d %H:%M:%S')

            query = Expense.update(Month=date_object.strftime('%B'), MadeBy=user, Transformed = 'Yes')
            query.execute()

            count += 1

        logger.info('Total rows transformed: {}'.format(count))

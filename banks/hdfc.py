import re
import os
import pandas as pd
from datetime import datetime
from banks.account import Account


class HDFC(Account):
    def __init__(self, filename):
        self.bank = "HDFC"
        self.prepare(filename)

    @staticmethod
    def clean_colon(s: str):
        return s.split(":")[1]

    @staticmethod
    def to_date(d: str, fullyear=False):
        """
        Example string: "01/03/22"
        """
        if fullyear:
            return datetime.strptime(d, "%d/%m/%Y")
        return datetime.strptime(d, "%d/%m/%y")

    def read_file(self, filename):
        df = pd.read_excel(filename, header=None)
        df.fillna("", inplace=True)

        return df

    def prepare_transactions(self, df):
        txns = []

        i = 22

        while True:
            txn = self.Transaction(
                date=self.to_date(self.clean(df.iloc[i][0])),
                description=self.clean(df.iloc[i][1]),
                ref=self.clean(df.iloc[i][2]),
                debit=self.to_float(self.clean(df.iloc[i][4])),
                credit=self.to_float(self.clean(df.iloc[i][5])),
                balance=self.to_float(self.clean(df.iloc[i][6])),
            )

            txns.append(txn)

            i += 1

            if self.clean(df.iloc[i][0]) == "":
                break

        return txns


    def prepare(self, filename):
        df = self.read_file(filename)

        account_name = self.clean(df.iloc[5][0])

        address = ""

        for i in range(6, 11):
            address += df.iloc[i][0] + " "

        address = self.clean(address)

        branch = self.clean(self.clean_colon(df.iloc[4][4]))
        account_number = self.clean(self.clean_colon(df.iloc[14][4]))

        se_dates = self.clean(df.iloc[15][0]).split("To")
        start_date = se_dates[0].split(":")[1].strip()
        end_date = se_dates[1].split(":")[1].strip()

        date_of_download = ""

        txns = self.prepare_transactions(df)

        self.account_name: str = account_name
        self.address: str = address
        self.account_number: str = self.clean_string2int(account_number)
        self.branch: str = branch
        self.start_date: str = self.to_date(start_date, fullyear=True)
        self.end_date: str = self.to_date(end_date, fullyear=True)
        self.date_of_download: str = date_of_download ## useless field in hdfc
        self.txns: List[self.Transaction] = txns

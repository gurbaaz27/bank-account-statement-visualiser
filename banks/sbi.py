import re
import os
import pandas as pd
from banks.account import Account


class SBI(Account):
    def __init__(self, filename):
        self.prepare(filename)

    def read_file(self, filename):
        with open(filename) as f:
            content = f.read()

        content = content.replace(",", "").replace("\t", ",")
        content = re.sub(" +", " ", content)

        nfilename = filename.split(".")[0] + ".csv"

        with open(nfilename, "w") as f:
            f.write(content)

        df = pd.read_csv(
            nfilename, sep=",", header=None, names=[0, 1, 2, 3, 4, 5, 6, 7]
        )
        df.fillna("-1", inplace=True)

        os.remove(nfilename)

        return df

    def prepare_transactions(self, df):
        txns = []

        i = 20

        while True:
            txn = self.Transaction(
                date=self.clean(df.iloc[i][0]),
                description=self.clean(df.iloc[i][2]),
                ref=self.clean(df.iloc[i][3]),
                debit=self.to_float(self.clean(df.iloc[i][4])),
                credit=self.to_float(self.clean(df.iloc[i][5])),
                balance=self.to_float(self.clean(df.iloc[i][6])),
            )

            txns.append(txn)

            i += 1

            # if self.clean(df.iloc[i][0]) == "-1":
            #     break

            if (
                self.clean(df.iloc[i][0])
                == "**This is a computer generated statement and does not require a signature"
            ):
                break

        return txns

    def prepare(self, filename):
        df = self.read_file(filename)

        account_name = self.clean(df.iloc[0][1])

        address = ""

        for i in range(1, 4):
            address += df.iloc[i][1] + " "

        address = self.clean(address)

        branch = self.clean(df.iloc[8][1])
        account_number = self.clean(df.iloc[6][1])

        start_date = self.clean(df.iloc[17][1])
        end_date = self.clean(df.iloc[18][1])

        date_of_download = self.clean(df.iloc[5][1])

        txns = self.prepare_transactions(df)

        self.account_name = account_name
        self.address = address
        self.account_number = self.clean_string2int(account_number)
        self.branch = branch
        self.start_date = self.to_date(start_date)
        self.end_date = self.to_date(end_date)
        self.date_of_download = self.to_date(date_of_download)
        self.txns = txns

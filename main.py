import re
import sys
import argparse
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter


def read_file(filename):
    """
    Download the account statement in excel format from SBI portal.
    Then replace all "," (commas) with "" (nil).
    Save the file in csv format using "Save As" or "Export to" option.
    """
    df = pd.read_csv(filename, sep="\t", header=None)

    df.fillna("-1", inplace=True)

    return df


def to_date(d: str):
    """
    Example string: "1 Mar 2022"
    """
    return datetime.strptime(d, "%d %b %Y")


def clean_string2int(s: str):
    """
    Example account number: "_00000011222333444"
    """
    return int(re.sub("[^0-9]", "", s))


def to_float(s: str):
    if s == "":
        return 0.0
    else:
        return float(s)


def clean(s: str):
    return " ".join(s.strip().split())


class Transaction:
    def __init__(
        self,
        date: str,
        description: str,
        ref: str,
        debit: float,
        credit: float,
        balance: float,
    ):
        self.date = to_date(date)
        self.description = description
        self.ref = ref
        self.debit = debit
        self.credit = credit
        self.balance = balance
        self.flow = credit - debit


class Account:
    def __init__(
        self,
        account_name: str,
        address: str,
        account_number: str,
        start_date: str,
        end_date: str,
        branch: str,
        date_of_download: str,
        txns,
    ):
        self.account_name = account_name
        self.address = address
        self.account_number = clean_string2int(account_number)
        self.branch = branch
        self.start_date = to_date(start_date)
        self.end_date = to_date(end_date)
        self.date_of_download = to_date(date_of_download)
        self.txns = txns


def prepare_transactions(df):
    txns = []

    i = 20

    while True:
        txn = Transaction(
            date=clean(df.iloc[i][0]),
            description=clean(df.iloc[i][2]),
            ref=clean(df.iloc[i][3]),
            debit=to_float(clean(df.iloc[i][4])),
            credit=to_float(clean(df.iloc[i][5])),
            balance=to_float(clean(df.iloc[i][6])),
        )

        txns.append(txn)

        i += 1

        if clean(df.iloc[i][0]) == "-1":
            break

    return txns


def prepare_account(df):
    account_name = clean(df.iloc[0][1])

    address = ""

    for i in range(1, 4):
        address += df.iloc[i][1] + " "

    address = clean(address)

    branch = clean(df.iloc[8][1])
    account_number = clean(df.iloc[6][1])

    start_date = clean(df.iloc[17][1])
    end_date = clean(df.iloc[18][1])

    date_of_download = clean(df.iloc[5][1])

    txns = prepare_transactions(df)

    account = Account(
        account_name=account_name,
        address=address,
        account_number=account_number,
        branch=branch,
        start_date=start_date,
        end_date=end_date,
        date_of_download=date_of_download,
        txns=txns,
    )

    return account


def prepare_plots(account: Account, account_name):

    money_map = {}

    for txn in account.txns:
        if txn.date in money_map.keys():
            money_map[txn.date] += txn.flow
        else:
            money_map[txn.date] = txn.flow

    prices = list(money_map.values())
    dates = list(money_map.keys())

    plt.style.use("dark_background")

    fig, ax = plt.subplots()

    clrs = ["red" if (price < 0) else "green" for price in prices]

    # plt.plot_date(dates, prices, color='#9b59b6', linestyle='-', ydate=False, xdate=True)
    plt.bar(
        dates, prices, align="center", color=clrs  # "#9b59b6"
    )  # , ydate=False, xdate=True)

    days = len(account.txns)
    if days <= 60:
        loc = mdates.WeekdayLocator()
    else:
        loc = mdates.MonthLocator()

    formatter = DateFormatter("%d %b")

    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(formatter)

    ax.yaxis.grid()

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    locs, _ = plt.yticks()
    ylabels = []
    for l in locs:
        lab = (
            str(int(l))
            .replace("000000000", "000M")
            .replace("00000000", "00M")
            .replace("0000000", "0M")
            .replace("000000", "M")
            .replace("00000", "00K")
            .replace("0000", "0K")
            .replace("000", "K")
        )
        if not ("K" in lab or "M" in lab):
            lab = "{:,}".format(int(lab))
        ylabels.append(lab)
    plt.yticks(locs, ylabels)

    if account_name:
        plt.figtext(0.6, 0.9, "Name: " + account.account_name)

    filename = (
        account.start_date.strftime("%d-%b")
        + "--"
        + account.end_date.strftime("%d-%b")
        + ".png"
    )

    plt.savefig(filename)  # , transparent=True)
    plt.close(fig)

    return filename


def main():
    try:
        DESCRIPTION = "Quickly view your expenses and earnings from account statement provided by SBI."
        parser = argparse.ArgumentParser(description=DESCRIPTION)
        parser.add_argument(
            "csvfile",
            type=str,
            help="Absolute path for your account statement csv file.\nDownload the account statement in excel format from SBI portal.\nThen replace all \",\" (commas) with \"\" (nil).\nSave the file in csv format using 'Save As' or 'Export to' option.",
        )
        parser.add_argument('--account-name', action='store_true', help="Annotate account name on the plot")

        args = parser.parse_args()

        df = read_file(args.csvfile)

        account = prepare_account(df)

        for k, v in account.__dict__.items():

            if k == "txns":
                continue

            key = " ".join(k.split("_"))
            value = v

            if type(v) == datetime:
                value = v.strftime("%d %B %Y")

            print(
                "{:<20} : {:<20}".format(
                    key.title(), value.title() if type(value) == str else value
                )
            )

        filename = prepare_plots(account, args.account_name)

        print(f"Plot has been saved successfully as {filename}")

        return 0

    except Exception as e:
        print(str(e))
        return -1


if __name__ == "__main__":
    sys.exit(main())

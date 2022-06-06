import re
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter


class Account:
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
            self.date = date
            self.description = description
            self.ref = ref
            self.debit = debit
            self.credit = credit
            self.balance = balance
            self.flow = credit - debit

    def __init__(self):
        pass

    @staticmethod
    def clean_string2int(s: str):
        """
        Example account number: "_00000011222333444"
        """
        return int(re.sub("[^0-9]", "", s))

    @staticmethod
    def to_float(s: str):
        if s == "":
            return 0.0
        else:
            return float(s)

    @staticmethod
    def clean(s: str):
        if isinstance(s, str):
            return " ".join(s.strip().split())
        else:
            return s

    def read_file(self, filename):
        """
        Download the account statement in excel format from your bank portal.
        """
        pass

    def prepare(self, df):
        pass

    def prepare_transactions(self, df):
        pass

    def prepare_plots(self, account_name):

        money_map = {}

        for txn in self.txns:
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

        days = len(self.txns)
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
            plt.figtext(0.6, 0.9, "Name: " + self.account_name)

        filename = (
            self.bank.lower()
            + "--"
            + self.start_date.strftime("%d-%b")
            + "--"
            + self.end_date.strftime("%d-%b")
            + ".png"
        )

        plt.savefig(filename)  # , transparent=True)
        plt.close(fig)

        return filename

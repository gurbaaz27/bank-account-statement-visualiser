import sys
import argparse
from datetime import datetime

from banks.sbi import SBI
from banks.hdfc import HDFC


def get_bank_account(bank: str, filename: str):
    if bank == "SBI":
        return SBI(filename)
    elif bank == "HDFC":
        return HDFC(filename)
    else:
        sys.exit("Invalid choice of bank. Current options: SBI, HDFC.")


def main():
    try:
        DESCRIPTION = "Quickly view your expenses and earnings from account statement provided by your bank."
        parser = argparse.ArgumentParser(description=DESCRIPTION)
        parser.add_argument(
            "bank",
            type=str,
            help="Your account statement's bank. Current options: SBI, HDFC",
        )
        parser.add_argument(
            "accountfile",
            type=str,
            help="Absolute path for your account statement xls file.\nDownload the account statement in excel format from your bank portal and use it here.",
        )
        parser.add_argument(
            "--account-name",
            action="store_true",
            help="Annotate account name on the plot",
        )

        args = parser.parse_args()

        account = get_bank_account(args.bank.upper(), args.accountfile)

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

        filename = account.prepare_plots(args.account_name)

        print(f"Plot has been saved successfully as {filename}")

        return 0

    except Exception as e:
        print(str(e))
        return -1


if __name__ == "__main__":
    sys.exit(main())

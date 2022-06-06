import re
import os
import pandas as pd
from banks.account import Account


class HDFC(Account):
    def __init__(self, filename):
        self.prepare(filename)

    def read_file(self, filename):
        pass

    def prepare(self, filename):
        pass

    def prepare_transactions(self, df):
        pass

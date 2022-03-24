# SBI Account Statement Visualiser

## Installation

```
git clone <repo>
cd <repo>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Help Log

```bash
python main.py --help

usage: main.py [-h] csvfile

Quickly view your expenses and earnings from account statement provided by SBI.

positional arguments:
  csvfile   Absolute path for your account statement csv file. Download the account statement in excel format 
            from SBI portal. Then replace all "," (commas) with "" (nil). Save the file in csv format using
            'Save As' or 'Export to' option.

optional arguments:
  -h, --help  show this help message and exit
```

## Demo Usage

```bash
python main.py <csvfile>

Account Name         : Xxxx   
Address              : Xxxx
Account Number       : Xxxx         
Branch               : Xxxx
Start Date           : 01 February 2022    
End Date             : 28 February 2022    
Date Of Download     : 23 March 2022       
Plot has been saved successfully as 01-Feb--28-Feb.png
```

![](assets/demo.jpg)
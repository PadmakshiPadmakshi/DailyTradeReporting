"""
# main.py
# 
# ******** Trading Report *********
# 1. Amount in USD settled incoming every day.
# 2. Amount in USD settled outgoing every day.
# 3. Ranking of entities based on incoming and outgoing amount.
# 
# Usage: python main.py < dataset.csv OR cat dataset.csv | python main.py
#
# Process data provided and print reports to standard output.
"""

from sys import stdin
from models import Reporting

def main():

    result = Reporting()
    result.add_data(stdin)

    print("=========================================================")
    print(result.report_amount_settled_every_day())
    print("=========================================================\n")
    print(result.report_rank_entities('incoming'))
    print("=========================================================\n")
    print(result.report_rank_entities('outgoing'))
    print("=========================================================\n")

    
if __name__ == '__main__':
    main()

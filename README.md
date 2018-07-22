# DailyTradeReporting

## Description
 This is a simple daily trade report for incoming instructions. Its takes set of instructions as input and generates a daily  report printed on console.

## Synopsis
 We can run this program either as `python main.py < dataset.csv` OR `cat dataset.csv | python main.py`

## Reporting Requirement
 (A) Given text data representing the instructions sent by various clients to execute in the international market. 
     Create a report that shows:
     
      - Amount in USD settled incoming every day
      - Amount in USD settled outgoing every day
      - Ranking of entities based on incoming and outgoing amount

  (B) Depending on the currency of each instruction the settlement date may be change. More specifically, Arabian has             different working days than the rest of the world. Therefore, a work week starts Monday and ends Friday, unless the         currency of the   trade is AED or SAR, where the work week starts Sunday and ends Thursday. No other holidays to be         taken into account.
  
## Approach & Assumptions
Finalized a simple approach with a few models files supporting main controller file. Thus eliminating any views/templates creation to present data. Also selected a recent version of Python i.e. Python3+ and tab-separated data file. 

Identified Instruction as one of the main objects, and distilled the overall task into three stages:

  1. Creating list of `Instruction` objects from the parsed dataset
  2. Analysing above list 
  3. Reporting

#### Framework
Created a virtual environment and stubs for the models, controller and test files. The main logic would be contained inside  methods of Reporting object e.g add_data() and other reporting methods which return the plain text report. The Reporting object will therefore contain the list of Instruction objects and it will manage that list and perform calculations. The main controller script will be responsible only for sending the data to it and printing reports.

#### Data Parsing
With the stubs in place I created dataset.csv file (with 2 given rows initially) and sending it into the stubs. I moved on to parsing the data and casting some values into their correct types. With that in place I was able to import the data into a list of Instructions within the Reporting object and output it to console. Furthermore created some more sample data to ensure parsing logic.

#### Data Adjustments
Created a methods to adjust settlement date if necessary (wrt requirement #B), and to add the USD amounts, and re-tested.

#### Data Analysis
Finally I added the _summarise_report() method to analyse the list into dicts keyed for required report. The analysis is separate from the add_data() method in the code so that it could be triggered separately or by a parameter option. This method is being called only once (i.e. we're ready to report data). Thus add_data() could be called multiple times, importing several datasets, with the overall analysis of that data deferred towards end.

#### Report Presentation
With the summary information available in dicts it just needs required formatting for each report.

## Generated Report

=========================================================

  AMOUNTS SETTLED EVERY DAY
  
     DATE         	   INCOMING (USD)	   OUTGOING (USD)
     04 Jan 2016  	             0.00	         10025.00
     07 Jan 2016  	         13244.00	             0.00
     08 Jan 2016  	             0.00	         79999.50
     11 Jan 2016  	         75633.60	             0.00
     12 Jan 2016  	             0.00	          9134.40
     18 Jan 2016  	        100593.50	             0.00

=========================================================

RANKING OF ENTITIES BASED ON INCOMING AMOUNT

      Rank	Entity          	             USD
         1	efg             	       100593.50
         2	xyz             	        75633.60
         3	bar             	        13244.00
         
=========================================================

RANKING OF ENTITIES BASED ON OUTGOING AMOUNT

      Rank	Entity          	             USD
         1	abc             	        79999.50
         2	foo             	        10025.00
         3	pqr             	         9134.40
         
=========================================================

## Assumptions
 - Python 3+
 - Data will contain a field delimiter (default tab), so that each record can be split()
 - Consistent list of field names as defined in the sample data
 - Consistent data types, format
 - The field names & other configuration information (e.g. workdays etc)

## Limitations
 - Hard-coded field names and globals for settlement date adjustments and USD calculations.
 - The object code has getattr/setattr style, and normal dot attribute style.
 - The test coverage is not comprehensive.
 - Rounding with format specifier .02f.


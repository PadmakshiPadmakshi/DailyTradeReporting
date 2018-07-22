"""
# models.py --- Module definition for trading reporting
# Models for working with Buy/Sell instructions.
# Contents: 
# 1) Instruction - Represent single buy/sell instructions.
# 2) Reporting - Create list of instructions from available dataset and reports.
#
"""

# Data fields
DATA_FIELDS = ['Entity','Buy/Sell','AgreedFx','Currency','InstructionDate',
               'SettlementDate','Units','Price per unit']

# Parsing dates and formatting output
DATE_FORMAT = '%d %b %Y' 

# Valid settlement weekdays and exceptions. (python weekday(), not isoweekday())
VALID_SETTLEMENT_DAYS_FOR_CURRENCY = {'AED': [6,0,1,2,3], 'SAR': [6,0,1,2,3], '_default': [0,1,2,3,4]}

# we need datetime to parse date strings and timedelta for SettlementDate updates
from datetime import datetime, timedelta

# helpers for casting incoming text values to required types
STR_TO_FLOAT = lambda _: float(_)
STR_TO_INT = lambda _: int(_)
STR_TO_DATE = lambda _: datetime.strptime(_, DATE_FORMAT).date()

# fields which need their values to be casted
CONVERSIONS = {'AgreedFx': STR_TO_FLOAT, 'Price per unit': STR_TO_FLOAT,
                    'InstructionDate': STR_TO_DATE, 'SettlementDate': STR_TO_DATE,
                    'Units': STR_TO_INT}


# the field & record separators to expect in the data
FIELD_SEP = "\t"
RECORD_SEP = "\n"


class Instruction:
    
    def __init__(self):
        """ Creating new instruction by setting placeholder attributes as dataset."""
        for field in DATA_FIELDS:
            setattr(self, field, None)
            
    def _getSettlementDate(self):
        try:
            working_days = VALID_SETTLEMENT_DAYS_FOR_CURRENCY[self.Currency]
        except KeyError:
            working_days = VALID_SETTLEMENT_DAYS_FOR_CURRENCY['_default']

        if len(working_days): # ensure we have at least one
            while self.SettlementDate.weekday() not in working_days:
                self.SettlementDate = self.SettlementDate + timedelta(days=1)

    def _addUSD(self):
        setattr(self, 'USD Amount',
                float('{usd:.02f}'.format(usd=getattr(self, 'Price per unit') *
                                         self.Units * self.AgreedFx)))
    def finalise(self):
        """Calculateing USD Amount by correcting settlement date (if necessary).
        """
        self._getSettlementDate()
        self._addUSD()

class Reporting:
    """Process the data and write result on console."""

    def __init__(self):
        """Create an object with an empty 'instruction(s)' list."""
        self.instructions = []

    def add_data(self, fh):
        """Iterate over file and append data to internal list."""
        for line in fh:
            if line.startswith(FIELD_SEP.join(DATA_FIELDS[:2])):
                continue # skip header lines   
            nextInstruction = Instruction()
            thisrow = [x.lstrip().rstrip() for x in line.split(FIELD_SEP)]
            for i in range(len(DATA_FIELDS)):
                key, val = DATA_FIELDS[i], thisrow[i] 
                try:
                    val = CONVERSIONS[key](val)
                except KeyError:
                    pass                 
                setattr(nextInstruction, key, val)

            nextInstruction.finalise() # adjust settlement date & add usd amount
            self.instructions.append(nextInstruction)
        self._summarise_report() # sort the data so we're ready to report on it

    def _summarise_report(self):
        """Loop through the current list of instructions and set an internal
        lists of totals by settlement date and by entity, for reporting.
        """

        # sort the instructions into (temporary) dicts with totals per date/entity
        self._by_date = {}
        self._by_entity = {"incoming": {},
                           "outgoing": {}}
        
        for instr in self.instructions:
            sdate = instr.SettlementDate
            buy_or_sell = getattr(instr, 'Buy/Sell')
            amount = getattr(instr, 'USD Amount')
            inout = 'outgoing' if buy_or_sell == 'B' else 'incoming'

            if sdate not in self._by_date:
                self._by_date[sdate] = {'incoming': 0.0,
                                        'outgoing': 0.0}
            
            self._by_date[sdate][inout] += amount
            try:
                self._by_entity[inout][instr.Entity] += amount
            except KeyError:
                self._by_entity[inout][instr.Entity] = amount

                
        # use those new dicts to create summary lists
        self._by_date_list = []
        for date in sorted(self._by_date.keys()):
            self._by_date_list.append([date,
                                        self._by_date[date]['incoming'],
                                        self._by_date[date]['outgoing']])

        for inout in ['incoming','outgoing']:
            setattr(self, '_by_entity_{}_list'.format(inout), [])
            
            for entity in sorted(self._by_entity[inout].keys(),
                                 key=lambda _: self._by_entity[inout][_],
                                 reverse=True):

                getattr(self, '_by_entity_{}_list'.format(inout)).\
                    append([entity, self._by_entity[inout][entity]])

                
        # delete those temporary dicts
        self._by_date = None
        self._by_entity = None


    def report_amount_settled_every_day(self):
        """Return a plain-text report on the amounts incoming & outgoing every
        day in the data.
        """
        str_format = FIELD_SEP.join(['{date:13s}','{incoming:>17s}','{outgoing:>17s}'])

        return "{headers}{sep}{data}".\
            format(headers="AMOUNTS SETTLED EVERY DAY{s}{s}".format(s=RECORD_SEP) +\
                   str_format.format(date='DATE',
                                     incoming='INCOMING (USD)',
                                     outgoing='OUTGOING (USD)'),
                   sep=RECORD_SEP,
                   data=RECORD_SEP.join([str_format.\
                                         format(date=_[0].strftime(DATE_FORMAT),
                                                incoming='{a:.02f}'.format(a=_[1]),
                                                outgoing='{a:.02f}'.format(a=_[2]))
                                         for _ in self._by_date_list]))

    
    def report_rank_entities(self, incoming_or_outgoing='incoming'):
        """Return a plain-text report on entities in the data, ranked by
        'outgoing' or 'incoming'.
        """
        return self._report_by_entity(incoming_or_outgoing)

    
    def _report_by_entity(self, in_or_out):
        str_format = FIELD_SEP.join(['{rank:>10s}','{entity:16s}','{amount:>16s}'])

        return "{title}{s}{headerline}{s}{data}".\
            format(title=("RANKING OF ENTITIES BASED ON {io} AMOUNT{se}".\
                          format(se=RECORD_SEP, io=in_or_out.upper())),
                   s=RECORD_SEP,
                   headerline=str_format.format(rank="Rank", entity="Entity", amount="USD"),
                   data=RECORD_SEP.join([str_format.\
                                         format(rank=str(x+1),
                                                entity=getattr(self,
                                                               '_by_entity_{}_list'.\
                                                               format(in_or_out))[x][0],
                                                amount='{a:.02f}'.\
                                                format(a=getattr(self,
                                                                 '_by_entity_{}_list'.\
                                                                 format(in_or_out))[x][1]))
                                         for x in range(len(getattr(self,'_by_entity_{}_list'.\
                                                                    format(in_or_out))))]))

from Strategy import Strategy
from Indicator import *
import random
import uuid


class StrategyBuilder:
    def __init__(self, indicators, risk_mgt_methods):
        self.max_entry_indicators = 2
        self.max_exit_indicators = 2
        self.max_risk_mgt_methods = 2
        self.indicators = indicators
        self.risk_mgt_methods = risk_mgt_methods

    def build_strategy(self):
        # Determine how many indicators and risk management methods to use
        num_entry_ind = random.randint(1, self.max_entry_indicators)
        num_exit_ind = random.randint(1, self.max_exit_indicators)
        num_risk_mgt = random.randint(0, self.max_risk_mgt_methods)

        # Select random indicators and risk management methods
        entry_indicators = random.sample(self.indicators, num_entry_ind)
        all_exit_indicators = [obj for obj in self.indicators if obj.is_exit_indicator is True]
        exit_indicators = random.sample(all_exit_indicators, num_exit_ind)
        risk_mgt_methods = random.sample(self.risk_mgt_methods, num_risk_mgt) if self.risk_mgt_methods else []

        # For each indicator, set random parameters based on threshold values
        for indicator in entry_indicators:
            indicator.setup(Side.ENTRY)
        for indicator in exit_indicators:
            indicator.setup(Side.EXIT)

        for method in risk_mgt_methods:
            method.randomize_parameters()

        # Create the strategy
        strategy = Strategy(
            id=str(uuid.uuid4()),
            entry_indicators=entry_indicators,
            exit_indicators=exit_indicators,
            risk_mgt_methods=risk_mgt_methods
        )

        return strategy






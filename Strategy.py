
class Strategy:
    def __init__(self, id, entry_indicators, exit_indicators, risk_mgt_methods):
        self.id = id
        self.entry_indicators = entry_indicators
        self.exit_indicators = exit_indicators
        self.risk_mgt_methods = risk_mgt_methods

    def get_details(self):
        description = "Strategy:\n"

        # Describe Entry Indicators
        description += "\nEntry Indicators:\n"
        for indicator in self.entry_indicators:
            description += f"- {indicator.name} (Cat: {indicator.category}, Type: {indicator.item_type}), Side: {indicator.side}\
                            Win1: ({indicator.window1}, Win2: {indicator.window2}, Win3: {indicator.window3}) \
                            Thrsh. Op: {indicator.threshold_operator}, Entry Thrsh: {indicator.entry_threshold}, Exit Thrsh: {indicator.exit_threshold})\n"

        # Describe Exit Indicators
        description += "\nExit Indicators:\n"
        for indicator in self.exit_indicators:
            description += f"- {indicator.name} (Category: {indicator.category}, Type: {indicator.item_type}), \
            Win1: ({indicator.window1}, Win2: {indicator.window2}, Win3: {indicator.window3}) \
            Thrsh. Op: {indicator.threshold_operator}, Entry Thrsh: {indicator.entry_threshold}, Exit Thrsh: {indicator.exit_threshold})\n"

        # Describe Risk Management Methods
        description += "\nRisk Management Methods:\n"
        for method in self.risk_mgt_methods:
            description += f"- {method.name} (Type: {method.item_type}), Threshold: {method.rm_threshold}\n"

        return description



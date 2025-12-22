class TechnicalParams:
    """技术指标参数配置"""

    def __init__(self, rsi_period: int = 14, macd_fast_period: int = 12, macd_slow_period: int = 26, macd_signal_period: int = 9, boll_period: int = 20, boll_std_dev: float = 2.0):
        self.rsi_period = rsi_period
        self.macd_fast_period = macd_fast_period
        self.macd_slow_period = macd_slow_period
        self.macd_signal_period = macd_signal_period
        self.boll_period = boll_period
        self.boll_std_dev = boll_std_dev

    @classmethod
    def default(cls) -> 'TechnicalParams':
        return cls()
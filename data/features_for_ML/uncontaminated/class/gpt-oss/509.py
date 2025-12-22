from dataclasses import dataclass

@dataclass
class TechnicalParams:
    """技术指标参数配置"""

    # 移动平均线
    ma_short: int = 5          # 短期均线周期
    ma_long: int = 20          # 长期均线周期

    # 相对强弱指数
    rsi_period: int = 14       # RSI 周期

    # 布林带
    bollinger_window: int = 20 # 布林带窗口
    bollinger_std: float = 2.0 # 布林带标准差倍数

    # MACD
    macd_fast: int = 12        # MACD 快速线周期
    macd_slow: int = 26        # MACD 慢速线周期
    macd_signal: int = 9       # MACD 信号线周期

    @classmethod
    def default(cls) -> 'TechnicalParams':
        """返回默认技术指标参数配置"""
        return cls()
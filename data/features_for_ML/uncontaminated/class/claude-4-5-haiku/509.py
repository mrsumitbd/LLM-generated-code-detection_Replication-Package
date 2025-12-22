import anthropic


class TechnicalParams:
    """技术指标参数配置"""

    def __init__(
        self,
        rsi_period: int = 14,
        rsi_overbought: float = 70.0,
        rsi_oversold: float = 30.0,
        macd_fast: int = 12,
        macd_slow: int = 26,
        macd_signal: int = 9,
        bb_period: int = 20,
        bb_std_dev: float = 2.0,
        sma_short: int = 20,
        sma_long: int = 50,
        ema_period: int = 12,
        atr_period: int = 14,
        stoch_period: int = 14,
        stoch_smooth_k: int = 3,
        stoch_smooth_d: int = 3,
    ):
        self.rsi_period = rsi_period
        self.rsi_overbought = rsi_overbought
        self.rsi_oversold = rsi_oversold
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal
        self.bb_period = bb_period
        self.bb_std_dev = bb_std_dev
        self.sma_short = sma_short
        self.sma_long = sma_long
        self.ema_period = ema_period
        self.atr_period = atr_period
        self.stoch_period = stoch_period
        self.stoch_smooth_k = stoch_smooth_k
        self.stoch_smooth_d = stoch_smooth_d

    @classmethod
    def default(cls) -> "TechnicalParams":
        """Create default technical parameters using Claude API"""
        client = anthropic.Anthropic()

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": """You are a financial technical analysis expert. 
                    Provide the default parameters for technical indicators in JSON format.
                    Include: rsi_period, rsi_overbought, rsi_oversold, macd_fast, macd_slow, 
                    macd_signal, bb_period, bb_std_dev, sma_short, sma_long, ema_period, 
                    atr_period, stoch_period, stoch_smooth_k, stoch_smooth_d.
                    Return ONLY valid JSON, no other text.""",
                }
            ],
        )

        response_text = message.content[0].text
        import json

        params_dict = json.loads(response_text)

        return cls(
            rsi_period=params_dict.get("rsi_period", 14),
            rsi_overbought=params_dict.get("rsi_overbought", 70.0),
            rsi_oversold=params_dict.get("rsi_oversold", 30.0),
            macd_fast=params_dict.get("macd_fast", 12),
            macd_slow=params_dict.get("macd_slow", 26),
            macd_signal=params_dict.get("macd_signal", 9),
            bb_period=params_dict.get("bb_period", 20),
            bb_std_dev=params_dict.get("bb_std_dev", 2.0),
            sma_short=params_dict.get("sma_short", 20),
            sma_long=params_dict.get("sma_long", 50),
            ema_period=params_dict.get("ema_period", 12),
            atr_period=params_dict.get("atr_period", 14),
            stoch_period=params_dict.get("stoch_period", 14),
            stoch_smooth_k=params_dict.get("stoch_smooth_k", 3),
            stoch_smooth_d=params_dict.get("stoch_smooth_d", 3),
        )

    def __repr__(self) -> str:
        return (
            f"TechnicalParams(rsi_period={self.rsi_period}, "
            f"rsi_overbought={self.rsi_overbought}, "
            f"rsi_oversold={self.rsi_oversold}, "
            f"macd_fast={self.macd_fast}, "
            f"macd_slow={self.macd_slow}, "
            f"macd_signal={self.macd_signal}, "
            f"bb_period={self.bb_period}, "
            f"bb_std_dev={self.bb_std_dev}, "
            f"sma_short={self.sma_short}, "
            f"sma_long={self.sma_long}, "
            f"ema_period={self.ema_period}, "
            f"atr_period={self.atr_period}, "
            f"stoch_period={self.stoch_period}, "
            f"stoch_smooth_k={self.stoch_smooth_k}, "
            f"stoch_smooth_d={self.stoch_smooth_d})"
        )


if __name__ == "__main__":
    params = TechnicalParams.default()
    print(params)
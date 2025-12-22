
class SeedEXState:
    """席德强化E释放的**当前**状态"""
    IDLE = "idle"  # 未开始强化E
    FIRST_CAST = "first"  # 第一段 (E_EX_0)
    LOOPING = "looping"  # 循环段 (E_EX_1)
    INTRUPTED = "interrupted"  # 中途打断 (E_EX_2)
    FINISH = "finish"  # 完整结束(SNA_1)
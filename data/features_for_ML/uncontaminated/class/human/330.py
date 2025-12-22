from ida_hexrays import (
    cexpr_t,
    cfuncptr_t,
    cinsn_t,
    citem_t,
    ctree_parentee_t,
)

class MemrefConstInfo:
    """Holds the parts of a `<var>.<mem at off> op <const number>` expression where op is either `=` or `==`."""

    var: cexpr_t
    mem_off: int
    value: int
    # noinspection PyTypeHints
    op: "Literal[ida_hexrays.cot_asg] | Literal[ida_hexrays.cot_eq]"
import os
from functools import wraps

def cgc_gff_option(func):
    """
    Decorator that reads a GFF file and passes a list of parsed records to the wrapped function.
    The wrapped function must accept the parsed GFF as its first positional argument.
    """
    @wraps(func)
    def wrapper(gff_path, *args, **kwargs):
        if not isinstance(gff_path, str):
            raise TypeError(f"Expected a file path string, got {type(gff_path).__name__}")
        if not os.path.exists(gff_path):
            raise FileNotFoundError(f"GFF file not found: {gff_path}")

        records = []
        with open(gff_path, "r", encoding="utf-8") as fh:
            for line_no, line in enumerate(fh, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("\t")
                if len(parts) != 9:
                    raise ValueError(
                        f"Line {line_no} in GFF file does not have 9 columns: {line}"
                    )
                seqid, source, type_, start, end, score, strand, phase, attributes = parts
                try:
                    start = int(start)
                    end = int(end)
                except ValueError:
                    raise ValueError(
                        f"Start or end not an integer on line {line_no}: {line}"
                    )
                # Parse attributes into a dict
                attr_dict = {}
                for attr in attributes.split(";"):
                    if not attr:
                        continue
                    if "=" in attr:
                        key, val = attr.split("=", 1)
                        attr_dict[key.strip()] = val.strip()
                    else:
                        attr_dict[attr.strip()] = None
                record = {
                    "seqid": seqid,
                    "source": source,
                    "type": type_,
                    "start": start,
                    "end": end,
                    "score": score,
                    "strand": strand,
                    "phase": phase,
                    "attributes": attr_dict,
                }
                records.append(record)

        return func(records, *args, **kwargs)

    return wrapper
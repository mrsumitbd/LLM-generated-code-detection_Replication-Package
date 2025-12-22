import csv
import io

class Ware:
    name: str
    description: str
    price: float

    def to_csv(self) -> str:
        with io.StringIO() as o:
            writer = csv.writer(o, quoting=csv.QUOTE_NONNUMERIC, lineterminator="\n")
            writer.writerow((self.name, self.description, self.price))
            return o.getvalue()
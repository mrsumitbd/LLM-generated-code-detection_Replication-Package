import tempfile

def __compress(result, target: str, power: int):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = f"{tmp_dir}/tmp.pdf"
        with open(tmp_file, "wb") as file:
            file.write(result)
        compress(tmp_file, target, power)
import datetime

def log(info):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now().isoformat()} - {info}\n")
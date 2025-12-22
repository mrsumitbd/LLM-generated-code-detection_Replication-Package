def log(info):
    with open("log.txt", "a") as log_file:
        log_file.write(f"{info}\n")
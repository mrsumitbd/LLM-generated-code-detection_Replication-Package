def log(info):
    with open('log.txt', 'a') as file:
        file.write(info + '\n')
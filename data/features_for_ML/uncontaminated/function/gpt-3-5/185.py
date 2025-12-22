def cgc_gff_option(func):
    def wrapper(*args, **kwargs):
        print("CGC GFF option is enabled")
        return func(*args, **kwargs)
    return wrapper
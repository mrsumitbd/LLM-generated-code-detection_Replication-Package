def cgc_gff_option(func):
    def wrapper(*args, **kwargs):
        if 'gff_file' in kwargs:
            gff_file = kwargs.pop('gff_file')
            with open(gff_file, 'r') as f:
                gff_data = f.read()
            kwargs['gff_data'] = gff_data
        return func(*args, **kwargs)
    return wrapper
def get_blend_data():
    import pandas as pd

    # Load the data from a CSV file
    df = pd.read_csv('blend_data.csv')

    # Perform any necessary data processing or transformation
    blend_data = df.to_dict('records')

    return blend_data
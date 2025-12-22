def prep(df):
    """
    Prepare a dataframe by handling missing values and encoding categorical variables.
    """
    import pandas as pd
    from sklearn.preprocessing import LabelEncoder
    
    # Create a copy to avoid modifying the original dataframe
    df = df.copy()
    
    # Handle missing values
    for col in df.columns:
        if df[col].dtype == 'object':
            # Fill missing categorical values with mode
            df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown', inplace=True)
        else:
            # Fill missing numerical values with median
            df[col].fillna(df[col].median(), inplace=True)
    
    # Encode categorical variables
    for col in df.columns:
        if df[col].dtype == 'object':
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
    
    return df
def prep(df):
    """
    Preprocess the input DataFrame by handling missing values, encoding categorical variables, and scaling numerical features.

    Args:
        df (pandas.DataFrame): The input DataFrame to be preprocessed.

    Returns:
        pandas.DataFrame: The preprocessed DataFrame.
    """
    import pandas as pd
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import LabelEncoder, StandardScaler

    # Handle missing values
    imputer = SimpleImputer(strategy='mean')
    df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

    # Encode categorical variables
    categorical_cols = df_imputed.select_dtypes(include='object').columns
    encoder = LabelEncoder()
    for col in categorical_cols:
        df_imputed[col] = encoder.fit_transform(df_imputed[col])

    # Scale numerical features
    numerical_cols = df_imputed.select_dtypes(exclude='object').columns
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df_imputed[numerical_cols]), columns=numerical_cols)

    # Combine the preprocessed features
    df_preprocessed = pd.concat([df_imputed[categorical_cols], df_scaled], axis=1)

    return df_preprocessed
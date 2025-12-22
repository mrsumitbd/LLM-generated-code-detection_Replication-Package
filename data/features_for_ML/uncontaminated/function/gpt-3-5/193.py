def extract_and_store_features(dataset, model, repo):
    features = model.extract_features(dataset)
    repo.store_features(features)
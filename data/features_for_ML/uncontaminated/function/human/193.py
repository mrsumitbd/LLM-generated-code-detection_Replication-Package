from annflux.repository.resultset import Resultset

def extract_and_store_features(dataset, model, repo):
    results_folder = model.validate(
        set_name=None,
        split_size=1024,
        dataset=dataset,
        compute_saliency=False,
        batch_size=256,
    )
    result_set = Resultset(results_folder)
    repo.commit(
        result_set, ancestors=[model, dataset], tag="unseen", allow_mixed_tags=True
    )
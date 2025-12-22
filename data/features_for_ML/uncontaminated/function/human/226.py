import torch
from . import variadic

def evaluate(pred, target, metrics, id2type):
    ranking, num_pred = pred
    type, answer_ranking, num_easy, num_hard = target

    metric = {}
    for _metric in metrics:
        if _metric == "mrr":
            answer_score = 1 / ranking.float()
            query_score = variadic.variadic_mean(answer_score, num_hard)
            type_score = variadic.native_scatter(query_score,
                                                 type,
                                                 dim_size=len(id2type),
                                                 reduce='mean')

        elif _metric.startswith("hits@"):
            threshold = int(_metric[5:])
            answer_score = (ranking <= threshold).float()
            query_score = variadic.variadic_mean(answer_score, num_hard)
            type_score = variadic.native_scatter(query_score,
                                                 type,
                                                 dim_size=len(id2type),
                                                 reduce='mean')
        elif _metric == "mape":
            query_score = (num_pred - num_easy - num_hard).abs() / (
                num_easy + num_hard
            ).float()
            type_score = variadic.native_scatter(query_score,
                                                 type,
                                                 dim_size=len(id2type),
                                                 reduce='mean')
        elif _metric == "spearmanr":
            type_score = []
            for i in range(len(id2type)):
                mask = type == i
                score = spearmanr(num_pred[mask], num_easy[mask] + num_hard[mask])
                type_score.append(score)
            type_score = torch.stack(type_score)
        elif _metric == "auroc":
            ends = (num_easy + num_hard).cumsum(0)
            starts = ends - num_hard
            target = variadic.multi_slice_mask(
                starts, ends, len(answer_ranking)
            ).float()
            answer_score = variadic_area_under_roc(
                answer_ranking, target, num_easy + num_hard
            )
            mask = (num_easy > 0) & (num_hard > 0)
            query_score = answer_score[mask]
            type_score = variadic.native_scatter(query_score,
                                                 type[mask],
                                                 dim_size=len(id2type),
                                                 reduce='mean')
        else:
            raise ValueError(f"Unknown metric `{_metric}`")

        score = type_score.mean()
        is_neg = torch.tensor(["n" in t for t in id2type], device=ranking.device)
        is_epfo = ~is_neg
        name = _metric
        for i, query_type in enumerate(id2type):
            metric[f"[{query_type}] {name}"] = type_score[i].item()
        if is_epfo.any():
            epfo_score = variadic.masked_mean(type_score, is_epfo)
            metric[f"[EPFO] {name}"] = epfo_score.item()
        if is_neg.any():
            neg_score = variadic.masked_mean(type_score, is_neg)
            metric[f"[negation] {name}"] = neg_score.item()
        metric[name] = score.item()

    return metric
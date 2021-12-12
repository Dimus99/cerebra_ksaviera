from api.controller_meaning import get_requests_by_mean, get_variants_by_mean
from api.controller_words import get_open_requests, get_variants


def get_mix_open_requests(text, limit=5):
    res_words = [{"title": l[2], "year": l[1], "FZ": l[3]} for l in
                 get_open_requests(text, limit)]

    res_means = [{"title": l[2], "year": l[1], "FZ": l[3]} for l in
                 get_requests_by_mean(text, limit)]

    res = []
    combine(limit, res, res_means, res_words)

    return res


def get_mix_projects(text, limit=5):
    res_words = [{"title": l[1], "description": l[2] if type(l[2]) == str else "", "company": l[3], "contact": l[4],
                  "phone": l[5], "FZ": l[6], "status": l[7]} for l in
                 get_variants(text, limit)]
    variants = get_variants_by_mean(text, limit)

    res_means = [{"title": l[1], "description": l[2] if type(l[2]) == str else "", "company": l[3], "contact": l[4],
                  "phone": l[5], "FZ": l[6], "status": l[7]}
                 for l in variants]
    res = []
    combine(limit, res, res_means, res_words)
    return res


def combine(limit, res, res_means, res_words):
    i1, i2 = 0, 0
    while len(res) != limit:
        while i1 < limit and res_means[i1] in res:
            i1 += 1
        while i2 < limit and res_words[i2] in res:
            i2 += 1
        if i1 <= i2 and i1 < limit:
            res.append(res_means[i1])
            i1 += 1
        else:
            res.append(res_words[i2])
            i2 += 1

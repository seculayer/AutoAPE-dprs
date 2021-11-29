from dprs.recommender.dp.MergeURLResCode import MergeURLResCode


def test_merge_url_res_code_type_1():
    tokenizer = MergeURLResCode(arg_list=[1])
    payload_list = [
        (["200", "/index.html"], ["200|/index.html"]),
        (["404", "/404.html"], ["404|/404.html"]),
        (["301", "example.com/index.html?q=none"], ["301|example.com/index.html"]),
    ]

    for payload, expected in payload_list:
        assert tokenizer.apply(payload) == expected


def test_merge_url_res_code_type_0():
    tokenizer = MergeURLResCode(arg_list=[0])
    data_list = [
        (["200", "GET /index.html"], ["200|/index.html"]),
        (["404", "GET /404.html"], ["404|/404.html"]),
        (["301", "GET example.com/index.html?q=none"], ["301|example.com/index.html"]),
    ]

    for payload, expected in data_list:
        assert tokenizer.apply(payload) == expected

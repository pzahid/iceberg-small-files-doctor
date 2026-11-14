from doctor.analyze import analyze, suggest, MB


def test_flags_many_small_files():
    r = analyze([1 * MB] * 8 + [128 * MB] * 2)
    assert r.small_files == 8 and r.severity == "high"
    assert "OPTIMIZE TABLE" in suggest("lake.t", r)


def test_healthy_table():
    r = analyze([120 * MB] * 10)
    assert r.severity == "low"
    assert suggest("lake.t", r).startswith("--")


def test_empty():
    assert analyze([]).severity == "none"

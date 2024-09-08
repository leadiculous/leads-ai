from classification import classify

items = [
    (
        "Landing page",
        "I need to create a landing page for my product. Cheapest template out there?",
        ["landing page"],
        True
    ),
    (
        "Hello",
        "Does anyone know a good landing page product?",
        ["landing page"],
        True
    ),
    (
        "An interesting title",
        "Who has the best landing page?",
        ["landing page"],
        True
    ),
    # Should still match because as a marketer I might be able to convince this user to use MY landing page product!
    (
        "I hate landing pages",
        "They are terrible",
        ["landing page"],
        True
    ),
    (
        "Best pizza",
        "Where can I get delicious pizza in NYC?",
        ["landing page"],
        False
    ),
]

for i, item in enumerate(items, 1):
    title = item[0]
    description = item[1]
    tags = item[2]
    expected = item[3]

    result = classify(title, description, tags)
    actual = result.classification

    print( f"Running test {i} '{title}'")
    print(result)

    assert actual == expected, f"❌ Fail: expected {expected}, but got {actual}"
    print(f"✅ Pass")

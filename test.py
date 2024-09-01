from zero_shot import predict

items = [
    ("I need to create a landing page for my product. Cheapest template out there?", True),
    ("Does anyone know a good landing page template?", True),
    ("I hate landing pages.", False),
    ("landing page", False),
    # ("Why do people like landing pages so much?", False)
    # ("Are landing pages over-hyped? I think so.", False)
]

for item in items:
    text = item[0]
    result = predict(text)
    actual = result['prediction']
    expected = item[1]
    assert actual == expected, f"❌ {text}"
    print(f"✅ {text}")

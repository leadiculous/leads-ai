import time

import torch
from transformers import pipeline

GPU_if_available = 0 if torch.cuda.is_available() else -1
classifier = pipeline(
    "zero-shot-classification",
    model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0",
    device=GPU_if_available
)


class ClassificationResult:
    def __init__(
            self,
            matched_topics: list[tuple[str, float]],
            score_threshold: float,
            execution_time: float,

    ):
        self.matched_topics = matched_topics
        self.score_threshold = score_threshold
        self.execution_time = execution_time

    def __str__(self):
        return str(self.__dict__)


def classify(title: str, description: str, topics: list[str]):
    start = time.time()
    result = classifier(
        f"{title}\n{description}",
        topics,
        hypothesis_template="This is an inquiry about {}",
        multi_label=True
    )
    end = time.time()
    execution_time = end - start

    score_threshold = 0.5
    matched_topics = [
        (label, score) for label,
        score in zip(result['labels'], result['scores'])
        if score > score_threshold
    ]

    return ClassificationResult(
        matched_topics if matched_topics else [],
        score_threshold,
        execution_time,
    )

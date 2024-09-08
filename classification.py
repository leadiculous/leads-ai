import stanza
import torch
from transformers import pipeline
import re

nlp = stanza.Pipeline('en', processors='tokenize')

GPU_if_available = 0 if torch.cuda.is_available() else -1
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=GPU_if_available)


class ClassificationResult:
    def __init__(
            self,
            matched_topics: list,
            is_relevant_topic: bool,
            is_exact_topic: bool,
            is_topic_found_in_question: bool,
            confidence_points: int,
            confidence_score: float
    ):
        self.matched_topics = matched_topics
        self.is_relevant_topic = is_relevant_topic
        self.is_exact_topic = is_exact_topic
        self.is_topic_found_in_question = is_topic_found_in_question
        self.confidence_points = confidence_points
        self.confidence_score = confidence_score

    def __str__(self):
        return str(self.__dict__)


def _split_into_sentences(text):
    doc = nlp(text)
    sentences = [sentence.text for sentence in doc.sentences]
    return sentences


def _match_topics(title, description, topics):
    post_content = f"Title: {title}\nDescription: {description}"
    result = classifier(post_content, topics, multi_label=True)
    confidence_threshold = 0.5
    matched_topics = [label for label, score in zip(result['labels'], result['scores']) if score > confidence_threshold]
    return matched_topics if matched_topics else []


def classify(title: str, description: str, tags: list):
    post_content = f"{title} {description}".lower()
    matched_topics = _match_topics(title, description, tags)

    confidence_points = 0

    # Determine whether the topic matches the post context using zero-shot classification
    is_relevant_topic = len(matched_topics) > 0
    if is_relevant_topic:
        confidence_points += 1

    # Check if the topic is textually mentioned in the post
    is_exact_topic = any(topic.lower() in post_content for topic in matched_topics)
    if is_exact_topic:
        confidence_points += 1

    # Check if the topic is textually mentioned in the form of a question
    sentences = [title] + _split_into_sentences(description)
    is_topic_found_in_question = any(
        re.search(r"(" + "|".join(matched_topics) + ").*\\?", sentence) for sentence in sentences) if len(
        matched_topics) > 0 else False
    if is_topic_found_in_question:
        confidence_points += 1

    confidence_score = round(confidence_points / 3, 2)

    return ClassificationResult(
        matched_topics,
        is_relevant_topic,
        is_exact_topic,
        is_topic_found_in_question,
        confidence_points,
        confidence_score
    )

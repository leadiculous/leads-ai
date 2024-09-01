import time

from transformers import pipeline

pipe = pipeline(model="facebook/bart-large-mnli")


# https://huggingface.co/tasks/zero-shot-classification
def predict(text: str):
    """
    Returns whether the text is an inquiry or not.
    Inquiries are texts that ask for information.
    :param text: The text to be classified.
    :return: A dictionary with the duration of the prediction (in milliseconds) and the prediction itself (True or False).
    """
    start = time.time()

    truthy = "inquiry"
    falsy = "no inquiry"

    prediction = pipe(
        text,
        candidate_labels=[truthy, falsy],
    )

    end = time.time()

    print(prediction)

    return {'duration': end - start, 'prediction': prediction['labels'][0] is truthy and prediction['scores'][0] > 0.8}

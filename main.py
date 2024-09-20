from concurrent import futures
import logging
import grpc
from service_pb2_grpc import ClassifierServicer, add_ClassifierServicer_to_server
from service_pb2 import ClassificationResponse, ClassificationRequest, Topic
from classification import classify


class Classifier(ClassifierServicer):
    def Classify(self, request: ClassificationRequest, context: grpc.ServicerContext) -> ClassificationResponse:
        request_topics = [topic for topic in request.topics]
        result = classify(request.title, request.body, request_topics)
        response_topics = [Topic(label=label, score=score) for label, score in result.matched_topics]
        return ClassificationResponse(
            matched_topics=response_topics,
            execution_time=result.execution_time,
            score_threshold=result.score_threshold,
        )


def serve():
    address = "localhost:50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ClassifierServicer_to_server(Classifier(), server)
    server.add_insecure_port(address)
    server.start()
    print(f"Server started on http://{address}")
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()

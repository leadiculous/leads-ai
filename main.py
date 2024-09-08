from concurrent import futures
import logging
import grpc
from service_pb2_grpc import ClassifierServicer, add_ClassifierServicer_to_server
from service_pb2 import ClassificationResponse, ClassificationRequest
from classification import classify


class Classifier(ClassifierServicer):
    def Classify(self, request: ClassificationRequest, context: grpc.ServicerContext) -> ClassificationResponse:
        tags = [tag for tag in request.tags]
        result = classify(request.title, request.body, tags)
        return ClassificationResponse(
            is_lead=result.is_relevant_topic,
            is_exact_topic=result.is_exact_topic,
            is_topic_found_in_question=result.is_topic_found_in_question,
            confidence_points=result.confidence_points,
            confidence_score=result.confidence_score,
            matched_topics=result.matched_topics,
            is_relevant_topic=result.is_relevant_topic,
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

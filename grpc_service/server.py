import os
import logging
from concurrent import futures

import grpc
from google.protobuf import empty_pb2
from google.protobuf.timestamp_pb2 import Timestamp

from app.db.session import SessionLocal
from app.core.config import settings
from app.crud.term import list_terms, get_term_by_keyword, create_term, update_term, delete_term
from app.schemas.term import TermCreate, TermUpdate

from grpc_service.generated import terms_pb2, terms_pb2_grpc


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _to_timestamp(dt) -> Timestamp:
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts


def _term_model_to_proto(term) -> terms_pb2.Term:
    return terms_pb2.Term(
        id=term.id,
        keyword=term.keyword,
        description=term.description,
        created_at=_to_timestamp(term.created_at),
        updated_at=_to_timestamp(term.updated_at),
    )


class TermsService(terms_pb2_grpc.TermsServiceServicer):
    def ListTerms(self, request: empty_pb2.Empty, context: grpc.ServicerContext) -> terms_pb2.ListTermsResponse:
        db = SessionLocal()
        try:
            terms = list_terms(db)
            return terms_pb2.ListTermsResponse(terms=[_term_model_to_proto(t) for t in terms])
        finally:
            db.close()

    def GetTerm(self, request: terms_pb2.GetTermRequest, context: grpc.ServicerContext) -> terms_pb2.Term:
        db = SessionLocal()
        try:
            term = get_term_by_keyword(db, request.keyword)
            if term is None:
                context.abort(grpc.StatusCode.NOT_FOUND, "Term not found")
            return _term_model_to_proto(term)
        finally:
            db.close()

    def CreateTerm(self, request: terms_pb2.CreateTermRequest, context: grpc.ServicerContext) -> terms_pb2.Term:
        if not request.keyword or not request.description:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Keyword and description are required")
        db = SessionLocal()
        try:
            existing = get_term_by_keyword(db, request.keyword)
            if existing is not None:
                context.abort(grpc.StatusCode.ALREADY_EXISTS, "Term with this keyword already exists")
            created = create_term(db, TermCreate(keyword=request.keyword, description=request.description))
            return _term_model_to_proto(created)
        finally:
            db.close()

    def UpdateTerm(self, request: terms_pb2.UpdateTermRequest, context: grpc.ServicerContext) -> terms_pb2.Term:
        if not request.keyword:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Keyword is required")
        db = SessionLocal()
        try:
            updated = update_term(db, request.keyword, TermUpdate(description=request.description or None))
            if updated is None:
                context.abort(grpc.StatusCode.NOT_FOUND, "Term not found")
            return _term_model_to_proto(updated)
        finally:
            db.close()

    def DeleteTerm(self, request: terms_pb2.DeleteTermRequest, context: grpc.ServicerContext) -> terms_pb2.DeleteTermResponse:
        if not request.keyword:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Keyword is required")
        db = SessionLocal()
        try:
            deleted = delete_term(db, request.keyword)
            if not deleted:
                context.abort(grpc.StatusCode.NOT_FOUND, "Term not found")
            return terms_pb2.DeleteTermResponse(deleted=True)
        finally:
            db.close()


def serve() -> None:
    host = os.getenv("GRPC_HOST", "0.0.0.0")
    port = int(os.getenv("GRPC_PORT", "50051"))
    settings.ensure_data_dir()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    terms_pb2_grpc.add_TermsServiceServicer_to_server(TermsService(), server)
    server.add_insecure_port(f"{host}:{port}")
    logger.info("Starting gRPC server on %s:%d", host, port)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()



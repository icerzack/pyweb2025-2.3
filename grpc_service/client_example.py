import argparse
import grpc
from google.protobuf import empty_pb2

from grpc_service.generated import terms_pb2, terms_pb2_grpc


def get_stub(address: str) -> terms_pb2_grpc.TermsServiceStub:
    channel = grpc.insecure_channel(address)
    return terms_pb2_grpc.TermsServiceStub(channel)


def cmd_list(stub: terms_pb2_grpc.TermsServiceStub) -> None:
    resp = stub.ListTerms(empty_pb2.Empty())
    for t in resp.terms:
        print(f"{t.id}\t{t.keyword}\t{t.description}")


def cmd_get(stub: terms_pb2_grpc.TermsServiceStub, keyword: str) -> None:
    t = stub.GetTerm(terms_pb2.GetTermRequest(keyword=keyword))
    print(f"{t.id}\t{t.keyword}\t{t.description}")


def cmd_create(stub: terms_pb2_grpc.TermsServiceStub, keyword: str, description: str) -> None:
    t = stub.CreateTerm(terms_pb2.CreateTermRequest(keyword=keyword, description=description))
    print(f"Created id={t.id} keyword={t.keyword}")


def cmd_update(stub: terms_pb2_grpc.TermsServiceStub, keyword: str, description: str) -> None:
    t = stub.UpdateTerm(terms_pb2.UpdateTermRequest(keyword=keyword, description=description))
    print(f"Updated id={t.id} keyword={t.keyword}")


def cmd_delete(stub: terms_pb2_grpc.TermsServiceStub, keyword: str) -> None:
    resp = stub.DeleteTerm(terms_pb2.DeleteTermRequest(keyword=keyword))
    print("Deleted" if resp.deleted else "Not deleted")


def main() -> None:
    parser = argparse.ArgumentParser(description="gRPC Terms client example")
    parser.add_argument("command", choices=["list", "get", "create", "update", "delete"]) 
    parser.add_argument("keyword", nargs="?")
    parser.add_argument("description", nargs="?")
    parser.add_argument("--address", default="localhost:50051")

    args = parser.parse_args()
    stub = get_stub(args.address)

    if args.command == "list":
        cmd_list(stub)
    elif args.command == "get":
        if not args.keyword:
            parser.error("get requires <keyword>")
        cmd_get(stub, args.keyword)
    elif args.command == "create":
        if not args.keyword or not args.description:
            parser.error("create requires <keyword> <description>")
        cmd_create(stub, args.keyword, args.description)
    elif args.command == "update":
        if not args.keyword or not args.description:
            parser.error("update requires <keyword> <description>")
        cmd_update(stub, args.keyword, args.description)
    elif args.command == "delete":
        if not args.keyword:
            parser.error("delete requires <keyword>")
        cmd_delete(stub, args.keyword)


if __name__ == "__main__":
    main()



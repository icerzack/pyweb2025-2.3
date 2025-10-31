#!/usr/bin/env python
from pathlib import Path
from grpc_tools import protoc
import pkg_resources


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    proto_dir = script_dir / "proto"
    out_dir = script_dir / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)

    include_dir = pkg_resources.resource_filename("grpc_tools", "_proto")

    args = [
        "",
        f"-I{proto_dir}",
        f"-I{include_dir}",
        f"--python_out={out_dir}",
        f"--grpc_python_out={out_dir}",
        str(proto_dir / "terms.proto"),
    ]

    protoc.main(args)


if __name__ == "__main__":
    main()



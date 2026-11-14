"""Run the standalone compiler on a non-conflicting localhost port."""

import os

import uvicorn


def main() -> None:
    uvicorn.run(
        "compiler_service.api:create_app",
        factory=True,
        host="127.0.0.1",
        port=int(os.environ.get("COMPILER_PORT", "8211")),
    )


if __name__ == "__main__":
    main()

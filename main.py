import asyncio
from src import FunPayUserParser
from src.config import setup_logger


async def main():
    # load logger settings
    setup_logger()

    parser = FunPayUserParser()
    await parser.get_all_users_by_range(from_index=1, to_index=10, step=1)


if __name__ == "__main__":
    asyncio.run(main=main())

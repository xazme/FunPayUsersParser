import httpx
import asyncio
import logging
from selectolax.parser import HTMLParser
from .user_dtos import UserResponseDTO

log = logging.getLogger(__name__)


class FunPayUserParser:
    def __init__(
        self,
        semaphores_count: int = 2,
        requests_delay: float = 0.9,
    ) -> None:
        self.__base_url = "https://funpay.com/users/"
        self.__semaphores = asyncio.Semaphore(semaphores_count)
        self.__delay = requests_delay
        self.__headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0",
        }

    async def get_all_users_by_range(
        self,
        from_index: int = 1,
        to_index: int = 1,
        step: int = 1,
    ) -> None:
        """
        Docstring for get_all_users_by_range

        :param self: Description
        :param filters: Description
        :type filters: UserFilters
        :param from_index: Description
        :type from_index: int
        :param to_index: Description
        :type to_index: int
        :param step: Description
        :type step: int
        """
        log.info("Ищу в диапозоне от %i до %i с шагом %i", from_index, to_index, step)

        async with httpx.AsyncClient(headers=self.__headers) as client:
            tasks = [
                asyncio.create_task(self.__get_user_by_id(client=client, id=i))
                for i in range(from_index, to_index + 1, step)
            ]

            for coro in asyncio.as_completed(tasks):
                result = await coro
                user = self.__extract_data(html=result.text)
                print(user.model_dump())
        log.info("Найденные данные были выведены")

    def __extract_data(
        self,
        html: str,
    ) -> UserResponseDTO:
        """
        Docstring for __extract_data

        :param self: Description
        :param html: Description
        :type html: str
        :return: Description
        :rtype: UserResponseDTO
        """
        tree = HTMLParser(html=html)
        username = self.__get_user_name(tree=tree)
        is_support = self.__is_user_support(tree=tree)
        is_banned = self.__is_user_banned(tree=tree)
        last_online = self.__get_last_online(tree=tree)

        return UserResponseDTO(
            name=username,
            is_support=is_support,
            is_banned=is_banned,
            last_online=last_online,
        )

    def __get_user_name(self, tree: HTMLParser) -> str | None:
        """
        Docstring for __get_user_name

        :param self: Description
        :param tree: Description
        :type tree: HTMLParser
        :return: Description
        :rtype: str | None
        """
        node = tree.css_first(query="span.mr4")
        return node.text(strip=True) if node else None

    def __is_user_support(self, tree: HTMLParser) -> bool:
        """
        Docstring for __is_user_support

        :param self: Description
        :param tree: Description
        :type tree: HTMLParser
        :return: Description
        :rtype: bool
        """
        node = tree.css_first(query="span.label.label-success")
        return True if node else False

    def __is_user_banned(self, tree: HTMLParser) -> bool:
        """
        Docstring for __is_user_banned
        :param self: Description
        :param tree: Description
        :type tree: HTMLParser
        :return: Description
        :rtype: bool
        """
        node = tree.css_first(query="span.label.label-danger")
        return True if node else False

    def __get_last_online(self, tree: HTMLParser) -> str | None:
        """
        Docstring for __get_last_online

        :param self: Description
        :param tree: Description
        :type tree: HTMLParser
        :return: Description
        :rtype: str | None
        """
        node = tree.css_first(query="span.media-user-status")
        return node.text(strip=True) if node else None

    async def __get_user_by_id(
        self,
        client: httpx.AsyncClient,
        id: int,
    ) -> httpx.Response:
        """
        Docstring for __get_user_by_id

        :param self: Description
        :param client: Description
        :type client: httpx.AsyncClient
        :param id: Description
        :type id: int
        :return: Description
        :rtype: Response
        """
        async with self.__semaphores:
            await asyncio.sleep(self.__delay)
            response = await client.get(url=self.__base_url + str(id) + "/")
            return response

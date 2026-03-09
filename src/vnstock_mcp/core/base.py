"""Base service with async execution patterns."""

import asyncio
from concurrent.futures import Executor
from typing import Callable, TypeVar

T = TypeVar("T")


class BaseService:
    """
    Base service class providing async execution patterns.

    Provides utility methods for running synchronous vnstock
    operations in an async context without blocking.
    """

    def _run_async(
        self,
        func: Callable[..., T],
        executor: Executor | None = None,
    ) -> "asyncio.Future[T]":
        """
        Run a synchronous function in an executor.

        Args:
            func: Synchronous function to run
            executor: Optional executor to use (None for default)

        Returns:
            Future that will contain the result
        """
        loop = asyncio.get_event_loop()
        return loop.run_in_executor(executor, func)

    async def run_sync(self, func: Callable[..., T]) -> T:
        """
        Run a synchronous function asynchronously.

        Args:
            func: Synchronous function to run

        Returns:
            Result of the function
        """
        return await self._run_async(func)
import asyncio
import inspect

import loguru


class BaseJob:
    def __init__(self, *args, **kwargs):
        self.logger = loguru.logger.bind(name=self.__class__.__name__)
        self.init(*args, **kwargs)

    def init(self):
        raise NotImplementedError

    def do_job(self):
        raise NotImplementedError

    def run(self):
        loop = asyncio.new_event_loop()
        loguru.logger.info(f"---->{self.__class__.__name__}")
        if inspect.iscoroutinefunction(self.do_job):
            # loguru.logger.info(f"------!")
            try:
                loop.run_until_complete(self.do_job())
                # asyncio.run(self.do_job())
            except Exception as e:
                self.report(e)
        else:
            try:
                self.do_job()
                # .run(self.do_job())
            except Exception as e:
                self.report(e)

    def report(self, e):
        loguru.logger.info(e)
        pass

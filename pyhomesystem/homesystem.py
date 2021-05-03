import asyncio
from aiohttp import web
import logging
import math
import time

"""
Setup a bone simple webserver, listen to POST's from a device like a
raspberry pi, decode results.
"""


HOMESYSTEM_LISTEN_PORT = 5199



class HomesystemListener:
    def __init__(self, port=HOMESYSTEM_LISTEN_PORT):
        # API Constants
        self.port = port

        # internal states
        self.server = None
        self.runner = None
        self.site = None
        self.r_listeners = []
        self.last_values = {}
        self.data_valid = False
        self.log = logging.getLogger(__name__)
        self.lastupd = 0

    def register_listener(self, function):
        self.r_listeners.append(function)


    async def handler(self, request: web.BaseRequest):
        if (request.method == 'POST'):
            data = await request.post()
            # data is not a dict, it's a MultiDict
            data_copy = {}
            for k in data.keys():
                data_copy[k] = data[k]
            self.last_values = data_copy.copy()
            self.data_valid = True
            self.lastupd = time.time()
            for rl in self.r_listeners:
                try:
                    await rl(data_copy)
                except:
                    pass

        return web.Response(text="OK")

    async def wait_for_valid_data(self):
        """ Wait for valid data, then return true. """
        while not self.data_valid:
            await asyncio.sleep(1)
        return self.data_valid

    async def listen(self):
        """ Listen and process."""

        self.server = web.Server(self.handler)
        self.runner = web.ServerRunner(self.server)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, port=self.port)
        await self.site.start()

        while True:
            await asyncio.sleep(10000)

    async def stop(self):
        await self.site.stop()

    async def start(self):
        loop = asyncio.get_event_loop()
        try:
            task = loop.create_task(self.listen())
            await task
        except Exception as e:
            self.log.error("Exiting listener {0}".format(str(e)))
        finally:
            loop.close()

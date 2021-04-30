import asyncio
from aiohttp import web
import logging
import math
import time
import datetime

"""
Setup a bone simple webserver, listen to POST's from a device.
"""


HOMESYSTEM_LISTEN_PORT = 5199


class HSListener:
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

        # slimme meter
        if "timestamp" in data:
            data["timestamp"] = datetime.datetime.fromtimestamp(int(data["m_in_1"])).strftime('%Y-%m-%d %H:%M:%S')
         if "m_in_1" in data:
            data["m_in_1"] = float(data["m_in_1"])
        if "m_in_2" in data:
            data["m_in_2"] = float(data["m_in_2"])
        if "m_out_1" in data:
            data["m_out_1"] = float(data["m_out_1"])
        if "m_out_2" in data:
            data["m_out_2"] = float(data["m_out_2"])
        if "m_you" in data:
            data["m_you"] = float(data["m_you"])
        if "v_in" in data:
            data["v_in"] = float(data["v_in"])
        if "v_out" in data:
            data["v_out"] = float(data["v_out"])
        if "v_you" in data:
            data["v_you"] = float(data["v_you"])
        if "v_eg" in data:
            data["v_eg"] = float(data["v_eg"])
        if "c_in" in data:
            data["c_in"] = float(data["c_in"])
        if "c_out" in data:
            data["c_out"] = float(data["c_out"])
        if "c_you" in data:
            data["c_you"] = float(data["c_you"])
        if "c_eg" in data:
            data["c_eg"] = float(data["c_eg"])

        # resol

        return(data)

    async def handler(self, request: web.BaseRequest):
        if (request.method == 'POST'):
            data = await request.post()
            # data is not a dict, it's a MultiDict
            data_copy = {}
            for k in data.keys():
                data_copy[k] = data[k]
            home_data = self.convert_units(data_copy)
            self.last_values = home_data.copy()
            self.data_valid = True
            self.lastupd = time.time()
            for rl in self.r_listeners:
                try:
                    await rl(home_data)
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

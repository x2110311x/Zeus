import aiohttp
import asyncio
import colorlog
import discord
import logging
import sys
import time

from discord.ext import commands

from . import exceptions
from .config import Config, ConfigDefaults
from .constants import VERSION
from .utilities import Utilities

log = logging.getLogger(__name__)

class ZeusBot(commands.Bot):
    def __init__(self, *, loop=None, config_file=None, command_prefix = None):
        if config_file is None:
            config_file = ConfigDefaults.config_file

        self.exit_signal = None

        self.config = Config(config_file)
        self._setup_logging()

        log.info(f'Starting Zeus Version - {VERSION}')

        commandPrefix = self.config.commandPrefix
        botIntents = discord.Intents.default()
        botIntents.members = True
        super().__init__(command_prefix=commandPrefix, intents=botIntents)
        self.aiosession = aiohttp.ClientSession(loop=self.loop)
        self.http.user_agent += f"Zeus{VERSION}"

    def _setup_logging(self):
        if len(logging.getLogger(__package__).handlers) > 1:
            log.debug("Skipping logger setup, already set up")
            return

        shandler = logging.StreamHandler(stream=sys.stdout)
        shandler.setFormatter(colorlog.LevelFormatter(
            fmt = {
                'DEBUG': '{log_color}[{levelname}:{module}] {message}',
                'INFO': '{log_color}{message}',
                'WARNING': '{log_color}{levelname}: {message}',
                'ERROR': '{log_color}[{levelname}:{module}] {message}',
                'CRITICAL': '{log_color}[{levelname}:{module}] {message}',

                'EVERYTHING': '{log_color}[{levelname}:{module}] {message}',
                'NOISY': '{log_color}[{levelname}:{module}] {message}',
                'VOICEDEBUG': '{log_color}[{levelname}:{module}][{relativeCreated:.9f}] {message}',
                'FFMPEG': '{log_color}[{levelname}:{module}][{relativeCreated:.9f}] {message}'
            },
            log_colors = {
                'DEBUG':    'cyan',
                'INFO':     'white',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'bold_red',

                'EVERYTHING': 'white',
                'EXTERNALAPI':     'bold_purple',
        },
            style = '{',
            datefmt = ''
        ))
        shandler.setLevel(self.config.debug_level)
        logging.getLogger(__package__).addHandler(shandler)

        log.debug("Set logging level to {}".format(self.config.debug_level))

        if self.config.debug_mode:
            dlogger = logging.getLogger('discord')
            dlogger.setLevel(logging.DEBUG)
            dhandler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
            dhandler.setFormatter(logging.Formatter('{asctime}:{levelname}:{name}: {message}', style='{'))
            dlogger.addHandler(dhandler)
    
    def _cleanup(self):
        try:
            self.loop.run_until_complete(self.logout())
            self.loop.run_until_complete(self.aiosession.close())
        except:
            pass

        pending = asyncio.Task.all_tasks()
        gathered = asyncio.gather(*pending)

        try:
            gathered.cancel()
            self.loop.run_until_complete(gathered)
            gathered.exception()
        except:
            pass

    def run(self):
        try:
            self.loop.run_until_complete(self.start(self.config.bottoken))
        except discord.errors.LoginFailure:
            log.critical("Could not login to Discord - Check your bot token")
        finally:
            try:
                self._cleanup()
            except Exception:
                log.error("Error while cleaning up", exc_info=True)
            
            if self.exit_signal:
                raise self.exit_signal

    async def on_error(self, event, *args, **kwargs):
        ex_type, ex, stack = sys.exc_info()
        if issubclass(ex_type, exceptions.Signal):
            self.exit_signal = ex_type
            await self.logout()
        else:
            log.error("Exception in {}".format(event), exc_info=True)

    async def on_command_error(self, context, exception):
        ex = exception.original
        ex_type = type(ex)
        if issubclass(ex_type, exceptions.Signal):
            self.exit_signal = ex_type
            log.info(f"Bot is shutting down - {self.exit_signal}")
            await self.logout()
        else:
            log.error("Exception in {}".format(context), exc_info=True)

    async def on_resumed(self):
        log.info("\nReconnected to discord.\n")
import logging
import configparser
import os
import shutil

log = logging.getLogger(__name__)
class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.find_file()
        self.check_fields()
        config = configparser.ConfigParser(interpolation=None)
        config.read(config_file, encoding="utf-8")

        sectioncompare = {"Credentials","Database","Logs","Gold","SocialMedia"}.difference(config.sections())
        if sectioncompare:
            raise Exception(
                "The config does not match the expected sections."
                "Please recreate it using the example_config from the GitHub Repo"
        )
        try:
            # Credentials
            self.bottoken = config.get("Credentials", "bot_token", fallback=ConfigDefaults.bottoken)

            self.lastfmtoken = config.get("Credentials", "lastFM_API_Key", fallback=ConfigDefaults.lastfmtoken)

            self.twitterAPIKey = config.get("Credentials", "lastFM_API_Key", fallback=ConfigDefaults.twitterAPIKey)
            self.twitterAPISecret = config.get("Credentials", "twitter_API_Secret", fallback=ConfigDefaults.twitterAPISecret)
            self.twitterAccessToken = config.get("Credentials", "twitter_Access_Token", fallback=ConfigDefaults.twitterAccessToken)
            self.twitterAccessSecret = config.get("Credentials", "twitter_Access_Secret", fallback=ConfigDefaults.twitterAccessSecret)

            self._youtubeAPIKey = config.get("Credentials", "youtube_API_Key", fallback=ConfigDefaults.youtubeAPIKey)

            # Database
            self.dbHost = config.get("Database", "hostname", fallback=ConfigDefaults.dbHost)
            self.dbName = config.get("Database", "database_name", fallback=ConfigDefaults.dbName)
            self.dbUser = config.get("Database", "username", fallback=ConfigDefaults.dbUser)
            self.dbpass = config.get("Database", "password", fallback=ConfigDefaults.dbpass)

            # Logs
            self.bot_log_channel = config.getint("Logs", "bot_logs", fallback=ConfigDefaults.bot_log_channel)
            self.delete_log_channel = config.getint("Logs", "delete_log", fallback=ConfigDefaults.delete_log_channel)
            self.edit_log_channel = config.getint("Logs", "edit_log", fallback=ConfigDefaults.edit_log_channel)
            self.join_log_channel = config.getint("Logs", "join_log", fallback=ConfigDefaults.join_log_channel)
            self.leave_log_channel = config.getint("Logs", "leave_log", fallback=ConfigDefaults.leave_log_channel)
            self.staffCommands_log_channel = config.getint("Logs", "staff_command_log", fallback=ConfigDefaults.staffCommands_log_channel)
            self.slur_log_channel = config.getint("Logs", "slur_log", fallback=ConfigDefaults.slur_log_channel)
            self.ban_log_channel = config.getint("Logs", "ban_log", fallback=ConfigDefaults.ban_log_channel)
            self.kick_log_channel = config.getint("Logs", "kick_log", fallback=ConfigDefaults.kick_log_channel)
            self.vc_log_channel = config.getint("Logs", "vc_log", fallback=ConfigDefaults.vc_log_channel)
            self.role_log_channel = config.getint("Logs", "role_log", fallback=ConfigDefaults.role_log_channel)

            # Gold
            self.gold_emoji = config.getint("Gold", "emoji_ID", fallback=ConfigDefaults.gold_emoji)
            self.gold_cost = config.getint("Gold", "cost", fallback=ConfigDefaults.gold_cost)
            self.gold_cooldown = config.getint("Gold", "cooldown", fallback=ConfigDefaults.gold_cooldown)
            self.gold_channel = config.getint("Gold", "gold_channel", fallback=ConfigDefaults.gold_channel)

            # Social Media
            self.twitterFeed_account = config.get("SocialMedia", "twitter_Account", fallback=ConfigDefaults.twitterFeed_account)
            self.twitterFeed_channel = config.getint("SocialMedia", "twitter_Feed", fallback=ConfigDefaults.twitterFeed_channel)
            self.youtubeFeed_account = config.get("SocialMedia", "youtube_Channel", fallback=ConfigDefaults.youtubeFeed_account)
            self.youtubeFeed_channel = config.getint("SocialMedia", "youtube_Feed", fallback=ConfigDefaults.youtubeFeed_channel)
            self.redditFeed_account = config.get("SocialMedia", "subreddit", fallback=ConfigDefaults.redditFeed_account)
            self.redditFeed_channel = config.getint("SocialMedia", "subreddit_Feed", fallback=ConfigDefaults.redditFeed_channel)
            self.instagramFeed_account = config.get("SocialMedia", "instagram_account", fallback=ConfigDefaults.instagramFeed_account)
            self.instagramFeed_channel = config.getint("SocialMedia", "instagram_Feed", fallback=ConfigDefaults.instagramFeed_channel)

            # Misc
            self.ownerID = config.get("Misc", "OwnerID", fallback=ConfigDefaults.ownerID)
            self.serverName = config.get("Misc", "serverName", fallback=ConfigDefaults.serverName)
            self.botName = config.get("Misc", "botName", fallback=ConfigDefaults.botName)

        except ValueError as e:
            log.critical(f"Error parsing config fields - likely an integer field missing or blank {e}")
            raise Exception("Error parsing config fields - likely an integer field missing or blank. Check log for more details")

    def get_all_keys(self, conf):
        """Returns all config keys as a list"""
        sections = dict(conf.items())
        keys = []
        for k in sections:
            s = sections[k]
            keys += [key for key in s.keys()]
        return keys

    def check_fields(self):
        config = configparser.ConfigParser(interpolation=None)
        config.read(self.config_file, encoding="utf-8")

        exConfig = configparser.ConfigParser(interpolation=None)

        if os.path.isfile(ConfigDefaults.exConfigFile):
            if not exConfig.read(ConfigDefaults.exConfigFile, encoding="utf-8"):
                log.info("Cannot read example config - cannot compare key list")
            else:
                configKeys = self.get_all_keys(config)
                exKeys = self.get_all_keys(exConfig)
                if set(configKeys) != set(exKeys):
                    missing_keys = set(exKeys) - set(configKeys)
                    print(f"Missing config keys - {missing_keys}")
        else:
            log.info("Example config not found - cannot compare key list")

    def find_file(self):
        config = configparser.ConfigParser(interpolation=None)
        if not os.path.isfile(self.config_file):
            if os.path.isfile(self.config_file + ".ini"):
                self.config_file = self.config_file + ".ini"
                log.info(f"Please add .ini to the config_file name")
            elif os.path.isfile("config/example_config.ini"):
                shutil.copy("config/example_config.ini", self.config_file)
                log.warning("Config was not found. Copying exmaple_config.ini")
            else:
                log.critical("The config file is missing. Please grab the example_config.ini from the GitHub Repo")
                raise Exception("The config file is missing. Please grab the example_config.ini from the GitHub Repo")
        
        if not config.read(self.config_file, encoding="utf-8"):
            log.critical("Could not open the config file. Please check it and try again")
            raise Exception("Could not open the config file. Please check it and try again")


class ConfigDefaults:
    # Example Config File
    exConfigFile = "config/example_config.ini"

    # Credentials
    bottoken = None

    lastfmtoken = None

    twitterAPIKey = None
    twitterAPISecret = None
    twitterAccessToken = None
    twitterAccessSecret = None

    youtubeAPIKey = None

    # Database
    dbHost = "localhost"
    dbName = "Zeus"
    dbUser = "Zeus"
    dbpass = None

    # Logs
    bot_log_channel = None
    delete_log_channel = None
    edit_log_channel = None
    join_log_channel = None
    leave_log_channel = None
    staffCommands_log_channel = None
    slur_log_channel = None
    ban_log_channel = None
    kick_log_channel = None
    vc_log_channel = None
    role_log_channel = None

    # Gold
    gold_emoji = None
    gold_cost = 500
    gold_cooldown = 0
    gold_channel = None

    # Social Media
    twitterFeed_account = None
    twitterFeed_channel = None
    youtubeFeed_account = None
    youtubeFeed_channel = None
    redditFeed_account = None
    redditFeed_channel = None
    instagramFeed_account = None
    instagramFeed_channel = None

    # Misc
    ownerID = 207129652345438211
    serverName = None
    botName = "Zeus"
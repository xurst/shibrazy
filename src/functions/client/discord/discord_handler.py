import discum
from dotenv import load_dotenv
import os
import re
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
from functions.client.message_handler import MessageChecker
import aiohttp
import asyncio
from datetime import datetime
import dateutil.parser
from core.constants import (
    SERVERS,
    TIMING,
    OUTPUT
)

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


class DiscordHandler:
    def __init__(self):
        self.bot = discum.Client(token=DISCORD_TOKEN, log=False, build_num=169669)
        self.server_channels = {}
        self.message_checker = MessageChecker()

        for server_id, config in SERVERS.items():
            self.server_channels[server_id] = list(config['channels'].keys())

    def get_latest_message(self, channel_id):
        try:
            messages = self.bot.getMessages(channelID=channel_id, num=1).json()
            if len(messages) > 0:
                return messages[0]
            return None
        except Exception as e:
            time.sleep(TIMING["rate_limit_delay"])
            return None

    def get_channel_config(self, server_id, channel_id):
        server_config = SERVERS.get(server_id)
        if server_config:
            return server_config['channels'].get(channel_id)
        return None

    def send_webhook_message(self, channel_name, message, matched_keywords=None):
        if not OUTPUT["webhook"]:
            return

        webhook_url = None
        channel_config = None

        # Find webhook URL and channel config
        for server_config in SERVERS.values():
            for channel_cfg in server_config['channels'].values():
                if channel_cfg['name'] == channel_name and 'webhook_url' in channel_cfg:
                    webhook_url = channel_cfg['webhook_url']
                    channel_config = channel_cfg
                    break
            if webhook_url:
                break

        if not webhook_url:
            print(f"\nNo webhook URL found for channel: {channel_name}")
            return

        try:
            webhook = DiscordWebhook(url=webhook_url)

            timestamp = message.get('timestamp', None)

            embed = DiscordEmbed(
                title="🔍 New Message Detected",
                color=0x2b2d31,
            )
            if timestamp:
                embed.set_timestamp(dateutil.parser.parse(timestamp).timestamp())

            avatar_url = f"https://cdn.discordapp.com/avatars/{message['author']['id']}/{message['author']['avatar']}.png" if \
                message['author'].get('avatar') else None

            embed.set_author(
                name=message['author']['username'],
                icon_url=avatar_url
            )

            embed.add_embed_field(
                name="📍 Location",
                value=f"Channel: {channel_name}",
                inline=True
            )

            embed.add_embed_field(
                name="👤 User ID",
                value=f"`{message['author']['id']}`",
                inline=True
            )

            embed.add_embed_field(
                name="⏰ Timestamp",
                value=f"{dateutil.parser.parse(timestamp).strftime('%B %d, %Y %H:%M:%S') if timestamp else 'Just now'}",
                inline=True
            )

            content = message['content']
            url = self.message_checker.extract_roblox_url(content, channel_config) if channel_config else None

            if url:
                content = content.replace(url, '').strip()

            if len(content) > 1024:
                content = content[:1021] + "..."

            embed.add_embed_field(
                name="💬 Message Content",
                value=f"```{content if content else 'No additional content'}```",
                inline=False
            )

            if url:
                embed.add_embed_field(
                    name="🔗 Game Link",
                    value=url,
                    inline=False
                )

            if matched_keywords:
                keyword_display = " • ".join(f"`{keyword}`" for keyword in matched_keywords)
                embed.add_embed_field(
                    name="🎯 Matched Keywords",
                    value=keyword_display,
                    inline=False
                )

            embed.set_footer(
                text="diddy was here",
                icon_url="https://cdn.discordapp.com/emojis/1039590248859627523.webp?size=96&quality=lossless"
            )

            webhook.add_embed(embed)
            response = webhook.execute()

        except Exception as e:
            print(f"Error sending webhook: {e}")

    async def cleanup(self):
        pass
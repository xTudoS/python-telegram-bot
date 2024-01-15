#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2023
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains an objects that are related to Telegram giveaways."""
import datetime
from typing import TYPE_CHECKING, Optional, Sequence, Tuple

from telegram._chat import Chat
from telegram._message import Message
from telegram._telegramobject import TelegramObject
from telegram._user import User
from telegram._utils.argumentparsing import parse_sequence_arg
from telegram._utils.datetime import extract_tzinfo_from_defaults, from_timestamp
from telegram._utils.types import JSONDict

if TYPE_CHECKING:
    from telegram import Bot


class Giveaway(TelegramObject):
    """This object represents a message about a scheduled giveaway.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`chats`, :attr:`winners_selection_date` and
    :attr:`winner_count` are equal.

    .. versionadded:: NEXT.VERSION

    Args:
        chats (Tuple[:class:`telegram.Chat`]): The list of chats which the user must join to
            participate in the giveaway.
        winners_selection_date (:class:`datetime.datetime`): The date when the giveaway winner will
            be selected. |datetime_localization|
        winner_count (:obj:`int`): The number of users which are supposed to be selected as winners
            of the giveaway.
        only_new_members (:obj:`True`, optional): If :obj:`True`, only users who join the chats
            after the giveaway started should be eligible to win.
        has_public_winners (:obj:`True`, optional): :obj:`True`, if the list of giveaway winners
            will be visible to everyone
        prize_description (:obj:`str`, optional): Description of additional giveaway prize
        country_codes (Sequence[:obj:`str`]): A list of two-letter ISO 3166-1 alpha-2
            country codes indicating the countries from which eligible users for the giveaway must
            come. If empty, then all users can participate in the giveaway. Users with a phone
            number that was bought on Fragment can always participate in giveaways.
        premium_subscription_month_count (:obj:`int`, optional): The number of months the Telegram
            Premium subscription won from the giveaway will be active for.

    Attributes:
        chats (Sequence[:class:`telegram.Chat`]): The list of chats which the user must join to
            participate in the giveaway.
        winners_selection_date (:class:`datetime.datetime`): The date when the giveaway winner will
            be selected. |datetime_localization|
        winner_count (:obj:`int`): The number of users which are supposed to be selected as winners
            of the giveaway.
        only_new_members (:obj:`True`): Optional. If :obj:`True`, only users who join the chats
            after the giveaway started should be eligible to win.
        has_public_winners (:obj:`True`): Optional. :obj:`True`, if the list of giveaway winners
            will be visible to everyone
        prize_description (:obj:`str`): Optional. Description of additional giveaway prize
        country_codes (Tuple[:obj:`str`]): Optional. A tuple of two-letter ISO 3166-1 alpha-2
            country codes indicating the countries from which eligible users for the giveaway must
            come. If empty, then all users can participate in the giveaway. Users with a phone
            number that was bought on Fragment can always participate in giveaways.
        premium_subscription_month_count (:obj:`int`): Optional. The number of months the Telegram
            Premium subscription won from the giveaway will be active for.
    """

    __slots__ = (
        "chats",
        "winners_selection_date",
        "winner_count",
        "only_new_members",
        "has_public_winners",
        "prize_description",
        "country_codes",
        "premium_subscription_month_count",
    )

    def __init__(
        self,
        chats: Sequence[Chat],
        winners_selection_date: datetime.datetime,
        winner_count: int,
        only_new_members: Optional[bool] = None,
        has_public_winners: Optional[bool] = None,
        prize_description: Optional[str] = None,
        country_codes: Optional[Sequence[str]] = None,
        premium_subscription_month_count: Optional[int] = None,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(api_kwargs=api_kwargs)

        self.chats: Tuple[Chat, ...] = tuple(chats)
        self.winners_selection_date: datetime.datetime = winners_selection_date
        self.winner_count: int = winner_count
        self.only_new_members: Optional[bool] = only_new_members
        self.has_public_winners: Optional[bool] = has_public_winners
        self.prize_description: Optional[str] = prize_description
        self.country_codes: Tuple[str, ...] = parse_sequence_arg(country_codes)
        self.premium_subscription_month_count: Optional[int] = premium_subscription_month_count

        self._id_attrs = (
            self.chats,
            self.winners_selection_date,
            self.winner_count,
        )

        self._freeze()

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: "Bot") -> Optional["Giveaway"]:
        """See :obj:`telegram.TelegramObject.de_json`."""
        data = cls._parse_data(data)

        if data is None:
            return None

        # Get the local timezone from the bot if it has defaults
        loc_tzinfo = extract_tzinfo_from_defaults(bot)

        data["chats"] = tuple(Chat.de_list(data.get("chats"), bot))
        data["winners_selection_date"] = from_timestamp(
            data.get("winners_selection_date"), tzinfo=loc_tzinfo
        )

        return super().de_json(data=data, bot=bot)


class GiveawayCreated(TelegramObject):
    """This object represents a service message about the creation of a scheduled giveaway.
    Currently holds no information.
    """

    __slots__ = ()


class GiveawayWinners(TelegramObject):
    """This object represents a message about the completion of a giveaway with public winners.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`chat`, :attr:`giveaway_message_id`,
    :attr:`winners_selection_date`, :attr:`winner_count` and :attr:`winners` are equal.

    .. versionadded:: NEXT.VERSION

    Args:
        chat (:class:`telegram.Chat`): The chat that created the giveaway
        giveaway_message_id (:obj:`int`): Identifier of the message with the giveaway in the chat
        winners_selection_date (:class:`datetime.datetime`): Point in time when winners of the
            giveaway were selected. |datetime_localization|
        winner_count (:obj:`int`): Total number of winners in the giveaway
        winners	(Sequence[:class:`telegram.User`]): List of up to
            :tg-const:`telegram.constants.GiveawayLimit.MAX_WINNERS` winners of the giveaway
        additional_chat_count (:obj:`int`, optional): The number of other chats the user had to
            join in order to be eligible for the giveaway
        premium_subscription_month_count (:obj:`int`, optional): The number of months the Telegram
            Premium subscription won from the giveaway will be active for
        unclaimed_prize_count (:obj:`int`, optional): Number of undistributed prizes
        only_new_members (:obj:`True`, optional): :obj:`True`, if only users who had joined the
            chats after the giveaway started were eligible to win
        was_refunded (:obj:`True`, optional): :obj:`True`, if the giveaway was canceled because the
            payment for it was refunded
        prize_description (:obj:`str`, optional): Description of additional giveaway prize

    Attributes:
        chat (:class:`telegram.Chat`): The chat that created the giveaway
        giveaway_message_id (:obj:`int`): Identifier of the message with the giveaway in the chat
        winners_selection_date (:class:`datetime.datetime`): Point in time when winners of the
            giveaway were selected. |datetime_localization|
        winner_count (:obj:`int`): Total number of winners in the giveaway
        winners	(Tuple[:class:`telegram.User`]): tuple of up to
            :tg-const:`telegram.constants.GiveawayLimit.MAX_WINNERS` winners of the giveaway
        additional_chat_count (:obj:`int`): Optional. The number of other chats the user had to
            join in order to be eligible for the giveaway
        premium_subscription_month_count (:obj:`int`): Optional. The number of months the Telegram
            Premium subscription won from the giveaway will be active for
        unclaimed_prize_count (:obj:`int`): Optional. Number of undistributed prizes
        only_new_members (:obj:`True`): Optional. :obj:`True`, if only users who had joined the
            chats after the giveaway started were eligible to win
        was_refunded (:obj:`True`): Optional. :obj:`True`, if the giveaway was canceled because the
            payment for it was refunded
        prize_description (:obj:`str`): Optional. Description of additional giveaway prize
    """

    __slots__ = (
        "chat",
        "giveaway_message_id",
        "winners_selection_date",
        "winner_count",
        "winners",
        "additional_chat_count",
        "premium_subscription_month_count",
        "unclaimed_prize_count",
        "only_new_members",
        "was_refunded",
        "prize_description",
    )

    def __init__(
        self,
        chat: Chat,
        giveaway_message_id: int,
        winners_selection_date: datetime.datetime,
        winner_count: int,
        winners: Sequence[User],
        additional_chat_count: Optional[int] = None,
        premium_subscription_month_count: Optional[int] = None,
        unclaimed_prize_count: Optional[int] = None,
        only_new_members: Optional[bool] = None,
        was_refunded: Optional[bool] = None,
        prize_description: Optional[str] = None,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(api_kwargs=api_kwargs)

        self.chat: Chat = chat
        self.giveaway_message_id: int = giveaway_message_id
        self.winners_selection_date: datetime.datetime = winners_selection_date
        self.winner_count: int = winner_count
        self.winners: Tuple[User, ...] = tuple(winners)
        self.additional_chat_count: Optional[int] = additional_chat_count
        self.premium_subscription_month_count: Optional[int] = premium_subscription_month_count
        self.unclaimed_prize_count: Optional[int] = unclaimed_prize_count
        self.only_new_members: Optional[bool] = only_new_members
        self.was_refunded: Optional[bool] = was_refunded
        self.prize_description: Optional[str] = prize_description

        self._id_attrs = (
            self.chat,
            self.giveaway_message_id,
            self.winners_selection_date,
            self.winner_count,
            self.winners,
        )

        self._freeze()

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: "Bot") -> Optional["GiveawayWinners"]:
        """See :obj:`telegram.TelegramObject.de_json`."""
        data = cls._parse_data(data)

        if data is None:
            return None

        # Get the local timezone from the bot if it has defaults
        loc_tzinfo = extract_tzinfo_from_defaults(bot)

        data["chat"] = Chat.de_json(data.get("chat"), bot)
        data["winners"] = tuple(User.de_list(data.get("winners"), bot))
        data["winners_selection_date"] = from_timestamp(
            data.get("winners_selection_date"), tzinfo=loc_tzinfo
        )

        return super().de_json(data=data, bot=bot)


class GiveawayCompleted(TelegramObject):
    """This object represents a service message about the completion of a giveaway without public
    winners.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`winner_count` and :attr:`unclaimed_prize_count` are equal.

    .. versionadded:: NEXT.VERSION


    Args:
        winner_count (:obj:`int`): Number of winners in the giveaway
        unclaimed_prize_count (:obj:`int`, optional): Number of undistributed prizes
        giveaway_message (:class:`telegram.Message`, optional): Message with the giveaway that was
            completed, if it wasn't deleted

    Attributes:
        winner_count (:obj:`int`): Number of winners in the giveaway
        unclaimed_prize_count (:obj:`int`): Optional. Number of undistributed prizes
        giveaway_message (:class:`telegram.Message`): Optional. Message with the giveaway that was
            completed, if it wasn't deleted
    """

    __slots__ = ("winner_count", "unclaimed_prize_count", "giveaway_message")

    def __init__(
        self,
        winner_count: int,
        unclaimed_prize_count: Optional[int] = None,
        giveaway_message: Optional["Message"] = None,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(api_kwargs=api_kwargs)

        self.winner_count: int = winner_count
        self.unclaimed_prize_count: Optional[int] = unclaimed_prize_count
        self.giveaway_message: Optional["Message"] = giveaway_message

        self._id_attrs = (
            self.winner_count,
            self.unclaimed_prize_count,
        )

        self._freeze()

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: "Bot") -> Optional["GiveawayCompleted"]:
        """See :obj:`telegram.TelegramObject.de_json`."""
        data = cls._parse_data(data)

        if data is None:
            return None

        data["giveaway_message"] = Message.de_json(data.get("giveaway_message"), bot)

        return super().de_json(data=data, bot=bot)

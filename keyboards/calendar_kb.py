import calendar
from datetime import datetime
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards import calendar_callback


def start_calendar(

        year: int = datetime.now().year,
        month: int = datetime.now().month
) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns InlineKeyboardMarkup object with the calendar.
    """
    inline_kb = InlineKeyboardMarkup(row_width=7)
    ignore_callback = calendar_callback.new("IGNORE", year, month, 0)  # for buttons with no answer
    # First row - Month and Year
    inline_kb.row()
    inline_kb.insert(InlineKeyboardButton(
        "<<",
        callback_data=calendar_callback.new("PREV-YEAR", year, month, 1)
    ))
    inline_kb.insert(InlineKeyboardButton(
        f'{calendar.month_name[month]} {str(year)}',
        callback_data=ignore_callback
    ))
    inline_kb.insert(InlineKeyboardButton(
        ">>",
        callback_data=calendar_callback.new("NEXT-YEAR", year, month, 1)
    ))
    # Second row - Week Days
    inline_kb.row()
    for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        inline_kb.insert(InlineKeyboardButton(day, callback_data=ignore_callback))

    # Calendar rows - Days of month
    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        inline_kb.row()
        for day in week:
            if (day == 0):
                inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
                continue
            inline_kb.insert(InlineKeyboardButton(
                str(day), callback_data=calendar_callback.new("DAY", year, month, day)
            ))

    # Last row - Buttons
    inline_kb.row()
    inline_kb.insert(InlineKeyboardButton(
        "<", callback_data=calendar_callback.new("PREV-MONTH", year, month, day)
    ))
    inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
    inline_kb.insert(InlineKeyboardButton(
        ">", callback_data=calendar_callback.new("NEXT-MONTH", year, month, day)
    ))

    return inline_kb

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# start - Start
# help - Get help
# setup - Setup this bot
# feedback - send me feedback :)

import pickle

from config.creds import TOKEN
from functions.bot import *


# Token for Bot


def reset_storage():
    knownUsers = []
    pickle.dump(knownUsers, open("./storage/knownUsers.txt", "wb"))
    userBooru = {}
    pickle.dump(userBooru, open("./storage/userBooru.txt", "wb"))
    userRating = {}
    pickle.dump(userRating, open("./storage/userRating.txt", "wb"))
    userTag = {}
    pickle.dump(userTag, open("./storage/userTag.txt", "wb"))
    userStep = {}
    pickle.dump(userStep, open("./storage/userStep.txt", "wb"))
    return userBooru, userRating, knownUsers, userTag


def load_storage():
    userBooru = pickle.load(open("./storage/userBooru.txt", "rb"))
    userRating = pickle.load(open("./storage/userRating.txt", "rb"))
    knownUsers = pickle.load(open("./storage/knownUsers.txt", "rb"))
    userTag = pickle.load(open("./storage/userTag.txt", "rb"))
    return userBooru, userRating, knownUsers, userTag


def main():
    # userBooru, userRating, knownUsers, userTag = reset_storage()
    userBooru, userRating, knownUsers, userTag = load_storage()

    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, workers=10)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("getSettings", getSettings))

    # CONVO Handlers:
    # Add conversation handler for Booru
    conv_settings = ConversationHandler(
        entry_points=[CommandHandler('setup', setup)],

        states={
            SETTINGS: [RegexHandler('^(ImageBoard|Rating|Tags)$', settings),
                       RegexHandler('^(Yande.re|e621|Gelbooru)$', booru),
                       RegexHandler('^(Safe|Questionable|Explicit|Not.Safe|Not.Questionable|Not.Explicit|Anything)$',
                                    rating),
                       RegexHandler('^(Yes|No)$', tags)
                       ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_settings)
    # Add conversation handler for Feedback
    conv_feedback = ConversationHandler(
        entry_points=[CommandHandler('feedback', feedback)],

        states={
            SENDFEEDBACK: [MessageHandler(Filters.text, sendFeedback)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_feedback)

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(poll_interval=0.1, timeout=20)

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

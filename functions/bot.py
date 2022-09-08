from uuid import uuid4

# Initialise Global Variables
SETTINGS = ()
SENDFEEDBACK = ()
defaultKeyboard = [['/setup', '/feedback']]
from telegram import *
from telegram.ext import *
from telegram.ext.dispatcher import run_async


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
# START!
def start(bot, update):
    """Send a message when the command /start is issued."""
    cid = update.message.chat.id
    update.message.reply_text('Hi ' + update.message.chat.first_name)
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        update.message.reply_text("I just finished setting you up")
        update.message.reply_text("By default I will search Yande.re for you")
        update.message.reply_text("And won't filter NSFW content")
        update.message.reply_text("now go chat with someone and mention me with @DelishBot")
        userBooru[cid] = 0;  # update existing entry
        userRating[cid] = 0;  # update existing entry
        userTag[cid] = 0;  # update existing entry
        userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getpic" command
        pickle.dump(knownUsers, open("./storage/knownUsers.txt", "wb"))
        pickle.dump(userBooru, open("./storage/userBooru.txt", "wb"))
        pickle.dump(userRating, open("./storage/userRating.txt", "wb"))
        pickle.dump(userTag, open("./storage/userTag.txt", "wb"))
    else:
        update.message.reply_text("I already know you xD")
        # pickle.dump( userBooru, open( "./storage/userBooru.txt", "wb" ) )
        # pickle.dump( knownUsers, open( "./storage/knownUsers.txt", "wb" ) )
        # pickle.dump( userStep, open( "./storage/userStep.txt", "wb" ) )


# HELP!
def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        "Use @delishbot and then enter search term, use _ for things that belong together (red_panda)")
    update.message.reply_text("Use /setup to change options")


# GET SETTINGS
def getSettings(bot, update):
    cid = update.message.chat.id
    update.message.reply_text("Booru:  " + str(userBooru[cid]))
    update.message.reply_text("Rating: " + str(userRating[cid]))
    update.message.reply_text("Tags: " + str(userTag[cid]))


# user can chose an image board
def setup(bot, update):
    reply_keyboard = [['ImageBoard', 'Rating', 'Tags']]
    update.message.reply_text("What would you want to Setup?",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                               resize_keyboard=True))  # show the keyboard
    return SETTINGS


# Display Keyboard by Cause
def settings(bot, update):
    user = update.message.from_user
    text = update.message.text
    update.message.reply_text('Editing: ' + update.message.text,
                              reply_markup=ReplyKeyboardMarkup(defaultKeyboard, one_time_keyboard=False,
                                                               resize_keyboard=True))
    logger.info("%s:%s", user.first_name, update.message.text)
    if text == "ImageBoard":
        reply_keyboard = [['e621', 'Yande.re', 'Gelbooru']]
        update.message.reply_text("Which Image Board do you want to use?",
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                   resize_keyboard=True))  # show the keyboard
        return SETTINGS
    if text == "Tags":
        reply_keyboard = [['Yes', 'No']]
        update.message.reply_text("Do you want tags displayed?",
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                   resize_keyboard=True))  # show the keyboard
        return SETTINGS
    if text == "Rating":
        reply_keyboard = [
            ['Safe', 'Questionable', 'Explicit', 'Not Safe', 'Not Questionable', 'Not Explicit', 'Anything']]
        update.message.reply_text("What Rating do you wan displayed?",
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                   resize_keyboard=True))  # show the keyboard
        return SETTINGS


# SET BOORUS
def booru(bot, update):
    user = update.message.from_user
    cid = user.id
    text = update.message.text
    logger.info("%s:%s", user.first_name, update.message.text)
    update.message.reply_text('The Image Board has been set to: ' + update.message.text,
                              reply_markup=ReplyKeyboardMarkup(defaultKeyboard, one_time_keyboard=False,
                                                               resize_keyboard=True))
    if text == "Yande.re":  # send the appropriate image based on the reply to the "/getImage" command
        userBooru[cid] = 0;  # update existing entry
        pickle.dump(userBooru, open("./storage/userBooru.txt", "wb"))
    elif text == "Gelbooru":
        userBooru[cid] = 1;  # update existing entry
        pickle.dump(userBooru, open("./storage/userBooru.txt", "wb"))
    elif text == "Delishbooru":
        userBooru[cid] = 2;  # update existing entry
        pickle.dump(userBooru, open("./storage/userBooru.txt", "wb"))
    elif text == "e621":
        userBooru[cid] = 3;  # update existing entry
        pickle.dump(userBooru, open("./storage/userBooru.txt", "wb"))
    return ConversationHandler.END


# SET RATING
def rating(bot, update):
    user = update.message.from_user
    cid = user.id
    text = update.message.text
    logger.info("%s:%s", user.first_name, update.message.text)
    if text == "Anything":
        update.message.reply_text("Everything will now be displayed",
                                  reply_markup=ReplyKeyboardMarkup(defaultKeyboard, one_time_keyboard=False,
                                                                   resize_keyboard=True))
        userRating[cid] = 0;  # update existing entry
    else:
        if text == "Not Safe":
            userRating[cid] = "-rating:safe";  # update existing entry
        elif text == "Not Questionable":
            userRating[cid] = "-rating:questionable";  # update existing entry
        elif text == "Not Explicit":
            userRating[cid] = "-rating:explicit";  # update existing entry
        else:
            userRating[cid] = "rating:" + text;  # update existing entry
        update.message.reply_text("Will now display: " + text,
                                  reply_markup=ReplyKeyboardMarkup(defaultKeyboard, one_time_keyboard=False,
                                                                   resize_keyboard=True))
    pickle.dump(userRating, open("./storage/userRating.txt", "wb"))
    return ConversationHandler.END


# SET TAGS
def tags(bot, update):
    user = update.message.from_user
    cid = user.id
    text = update.message.text
    logger.info("%s:%s", user.first_name, update.message.text)
    if text == "Yes" or text == "yes":
        # update.message.reply_text("Tags!", reply_markup=defaultMenu)
        update.message.reply_text("Tags!", reply_markup=ReplyKeyboardMarkup(defaultKeyboard, one_time_keyboard=False,
                                                                            resize_keyboard=True))
        userTag[cid] = 0;  # update existing entry
        pickle.dump(userTag, open("./storage/userTag.txt", "wb"))
    elif text == "No" or text == "no":
        update.message.reply_text("No tags!", reply_markup=ReplyKeyboardMarkup(defaultKeyboard, one_time_keyboard=False,
                                                                               resize_keyboard=True))
        userTag[cid] = 1;  # update existing entry
        pickle.dump(userTag, open("./storage/userTag.txt", "wb"))
    return ConversationHandler.END


# Cancel Conversation
def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the operation.", user.first_name)
    update.message.reply_text('Settings canceled.',
                              reply_markup=ReplyKeyboardMarkup(defaultKeyboard, one_time_keyboard=False,
                                                               resize_keyboard=True))
    return ConversationHandler.END


# handle the "/feedback" command
def feedback(bot, update):
    update.message.reply_text("What feedback would you want to send to my owner?")
    update.message.reply_text("Or /cancel to stop")
    return SENDFEEDBACK


# if the user has issued the "/feedback" command, process the answer
def sendFeedback(bot, update):
    feedbackID = 35070363  # IMLinus
    user = update.message.from_user
    cid = user.id
    username = "Username: " + user.username
    userCID = "CID: " + str(cid)
    text = "Feedback: " + update.message.text
    bot.send_message(feedbackID, "Hello Master, there is Feedback for you:")
    bot.send_message(feedbackID, username)
    bot.send_message(feedbackID, userCID)
    bot.send_message(feedbackID, text)
    update.message.reply_text("Feedback sent ;)")
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


# INLINE QUERY!
@run_async
def inlinequery(bot, update):
    # Get User ID from Query
    cid = update.inline_query.from_user.id
    username = update.inline_query.from_user.username
    search = update.inline_query.query
    offset = update.inline_query.offset
    answerArray = []
    if not offset:
        offset = 0
    # Get Booru from Save
    booru = userBooru.get(cid, "empty")
    if booru == "empty":
        userBooru[cid] = 0;  # update existing entry
        pickle.dump(userBooru, open("./storage/userBooru.txt", "wb"))
        booru == 0
    else:
        booru == userBooru[cid]
    # Get Tag or not from Save
    tagging = userTag.get(cid, "empty")
    if tagging == "empty":
        userTag[cid] = 0;  # update existing entry
        pickle.dump(userTag, open("./storage/userTag.txt", "wb"))
        tagging == 0
    else:
        tagging == userTag[cid]
    # Get Rating from Save
    rating = userRating.get(cid, "empty")
    if rating == "empty":
        userRating[cid] = 0;  # update existing entry
        pickle.dump(userRating, open("./storage/userRating.txt", "wb"))
        rating == 0
    if rating == 1:
        userRating[cid] = 0;  # update existing entry
        pickle.dump(userRating, open("./storage/userRating.txt", "wb"))
        rating == 0
    else:
        rating == userBooru[cid]

    # logger.info("Booru: %s",booru)
    # logger.info("Rating: %s",rating)
    # logger.info("Tagging: %s",tagging)

    # Start the image searcher, returns three arrays, unless there was an error.
    urls, thumbs, tags = getImages(cid, search, booru, rating, offset, username)
    # logger.info("URLS: %s",urls)
    # logger.info("thumbs: %s",thumbs)
    # logger.info("tags: %s",tags)

    if urls == 0:
        try:
            r = [
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="Sorry, no results",
                    input_message_content=InputTextMessageContent("Sorry, no results"))]
            update.inline_query.answer(r, is_personal=True, cache_time=30)
        except Exception as e:
            print(e)
    elif urls == 1:
        try:
            r = [
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="Sorry, API Error",
                    input_message_content=InputTextMessageContent("Sorry, API Error"))]
            update.inline_query.answer(r, is_personal=True, cache_time=30)
        except Exception as e:
            print(e)
    else:
        # prepare Lists for the shortened URLs
        shortUrls = list()
        shortThumbs = list()

        # Fill url Lists
        for x in range(0, len(urls)):
            # short = goo_shorten_url(urls[x])
            short = urls[x]
            shortUrls.append(short)
        for x in range(0, len(thumbs)):
            # short = goo_shorten_url(thumbs[x])
            short = thumbs[x]
            shortThumbs.append(short)
        try:
            if tagging == 0:
                for x in range(0, len(urls)):
                    answerArray.append(InlineQueryResultPhoto(
                        id=str(x + int(offset)),
                        photo_url=shortUrls[x],
                        thumb_url=shortThumbs[x],
                        caption=tags[x]
                    ))
            else:
                for x in range(0, len(urls)):
                    answerArray.append(InlineQueryResultPhoto(
                        id=str(x + int(offset)),
                        photo_url=shortUrls[x],
                        thumb_url=shortThumbs[x],
                    ))
            update.inline_query.answer(answerArray, is_personal=True, cache_time=30,
                                       next_offset=int(offset) + len(urls))
        except Exception as e:
            print(e)
            print
            "Failure with sending pics"

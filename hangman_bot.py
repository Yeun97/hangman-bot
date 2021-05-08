import discord

client = discord.Client()

# the text channel to send messages to
channel = ""

# the word to guess
magic_word = "start"

# letters that have been guessed correctly
guessed_letters = ""

# letters that have been guessed incorrectly
wrong_letters = ""

# 7 strikes and the game is over
strikes = 0

# previous admin
prev_admin = ""

# whoever guesses the word becomes the word_chooser
word_chooser = ""

# only let the word_chooser set a new word right after the word has been guessed
word_setting_time = False

# don't let people guess after the word is found
guessing_time = True

# get the text channel the bot will send messages to
@client.event
async def on_ready():
    global channel
    channel = client.get_channel(613152433517887517)
    print('We have logged in as {0.user}'.format(client))


# called when the bot receives any message
@client.event
async def on_message(message):
    # ignore messages from itself
    if message.author == client.user:
        return

    global magic_word
    global guessed_letters
    global wrong_letters
    global strikes
    global word_chooser
    global word_setting_time
    global guessing_time

    # guessing a letter
    if message.content.startswith('!letter'):
        # they have to write something after !letter
        if (len(message.content.split()) > 1):

            letter = message.content.split()[1]

            # the letter has to be one letter and the word_chooser can't guess
            if (len(letter) == 1 & guessing_time & ((prev_admin == "")  | (message.author != prev_admin))):
                # guessed a correct letter
                if (letter.lower() in magic_word):
                    guessed_letters += letter

                # guessed a wrong letter
                else:
                    wrong_letters += letter + ", "
                    strikes += 1

                await print_hangman()


    # if the user guesses the magic word, send them a pm to let them choose the new word,
    # and let the others in the server know that the word was guessed
    elif message.content.startswith('!guess'):
        if (len(message.content.split()) > 1):
            guess = message.content.split()[1]

            if (guessing_time & ((prev_admin == "")  | (message.author != prev_admin))):
                if (magic_word == guess.lower()):
                    word_chooser = message.author
                    word_setting_time = True
                    guessing_time = False
                    guessed_letters = ""
                    wrong_letters = ""
                    strikes = 0

                    await word_chooser.send('You guessed the word: \"' + magic_word + '\"!\n' + 'Please type !new_word (your word) to set the new magic word!\n' + 'example: !new_word hello')
                    await channel.send(message.author.name + ' has guessed the word: \"' + magic_word + '\"!\n' + 'Now waiting for the new word to be chosen...')
                else:
                    strikes += 1
                    await print_hangman()

    # setting the new magic word and changing admins
    elif message.content.startswith('!new_word') & (message.author == word_chooser) & word_setting_time:
            magic_word = message.content.split()[1].lower()
            word_setting_time = False
            guessing_time = True

            await make_admin()

            await word_chooser.send('You have set the word to: ' + magic_word + '!')
            await channel.send(message.author.name + ' has chosen a new word!\n' + 'Guess the word to take their admin role')


async def print_hangman():
    global guessed_letters
    global wrong_letters
    global strikes
    global word_setting_time
    global guessing_time

    # pick which hangman stage to show based on the strikes
    switcher = {
        1: "hangman_stage1.png",
        2: "hangman_stage2.png",
        3: "hangman_stage3.png",
        4: "hangman_stage4.png",
        5: "hangman_stage5.png",
        6: "hangman_stage6.png",
        7: "hangman_stage7.png"
    }

    await channel.send(file=discord.File(switcher.get(strikes, "hangman_stage0.png")))

    # show the guessed letters and the wrong letters
    partial_word = ""

    for c in magic_word:
        if (c in guessed_letters):
            partial_word += c + " "
        else:
            partial_word += "? "

    # wrong letters minus the extra comma at the end
    display_wrong_letters = ""

    if (len(wrong_letters) > 0):
        display_wrong_letters = wrong_letters[:-2]

    await channel.send(partial_word + "\nwrong letters: " + display_wrong_letters)

    # reset the game after 7 strikes
    if (strikes >= 7):
        word_setting_time = True
        guessing_time = False
        strikes = 0
        guessed_letters = ""
        wrong_letters = ""

        await channel.send("You guys suck. The word was " + magic_word + ".\nNow wait for " + word_chooser.name + " to pick a new word")
        await word_chooser.send('Pick a new word because your friends are dumb\nexample: !new_word hello')

# makes the word_chooser admin, and un-admins the last admin
async def make_admin():
    global prev_admin

    if prev_admin != "":
        await prev_admin.remove_roles(client.guilds[0].get_role(800618773547057152))

    await word_chooser.add_roles(client.guilds[0].get_role(800618773547057152))
    prev_admin = word_chooser



client.run('ODQwMTM0ODYyMzAzMjY0NzY4.YJTykA.X7t869SdvEXBG-aXtddi_jc3ftk')

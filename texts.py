class EN:
    SUCCESS_SERVER_CONFIGURED = "The server has been configured successfully"
    SUCCESS_SERVER_RESET = "The configuration has been deleted"
    ERROR_NOT_CONFIGURED="Error: There is no tournament configured"
    ERROR_ALREADY_CONFIGURED = "Error: The server is already configured"
    ERROR_NOT_ALLOWED = "Error: Only server admins can do this action"
    ERROR_DATA_NOT_FOUND = "Error: Data not found. Remember to follow the configuration steps. If you have already done so, it may take a few hours the first time to retrieve your league data. Try it again later."
    ERROR_NOT_SCHEDULE = "Error: This type of tournament does not have a schedule"
    ERROR_SYNTAX_CONFIGURATION = "Error: Invalid syntax. Please, use ```bb2!configure \"league name\" \"tournament name\"```, including the quotes, to configure your server."
    ERROR_SYNTAX_IAM = "Error: Invalid syntax. Please, use ```bb2!iam {your coach name}``` to link your discord account to your coach name"

    BOT_THUMBAIL = "https://i.imgur.com/8eptQlM.png"

    HELP_GENERIC_TITLE = "Blood Bowl Manager"
    HELP_GENERIC_DESCRIPTION = "To see a page, just add the page number after the bb2!help command.\nLike this: ```bb2!help 2```"
    HELP_GENERIC_FIELDS = [
        ("Chapter 1: Set up your tournament", "Check the firsts steps on Blood Bowl Bot")
        ,("Chapter 2: Blood Bowl Commands", "Check the available commands on Blood Bowl Bot after configure your tournament")
    ]

    HELP_SETUP_TITLE = "Setup - Blood Bowl Manager"
    HELP_SETUP_DESCRIPTION = "Follow the next steps to configure your tournament on the discord server"
    HELP_SETUP_FIELDS = [
        ("#1 Allow GoblinSpy recover data from your tournament.", "Join http://www.mordrek.com/goblinSpy/web/activate.html?, introduce your tournament data and click on \"Activate\" button.")
        ,("#2 Configure the tournament on the bot", "Use ```bb2!config \"League name\" \"Tournament name\"```, including quotation marks, to configure the tournament.")
        ,("#3 Install the custom emojis", "Install the following emoji package on your server with the races icons")
    ]

    HELP_COMMAND_TITLE = "Commands - Blood Bowl Manager"
    HELP_COMMAND_DESCRIPTION = "Use the following commands to get info about the configured tournament. Newly played matches may take a while to update."
    HELP_COMMAND_FIELDS = [
        ("```bb2!teams```", "List all teams from the tournament"),
        ("```bb2!round <round number>```", "Show the matches of the selected round. If no round is specified, it will show the current round."),
        ("```bb2!iam <coach name>```", "Link your Discord acc to your BloodBowl nickname, changing the coach name by your discord id on the messages.")
        ]
    ROUND= "Round %s"
    LAST_UPDATE = "Last update at %s"
    LOCAL_TEAM = "Local Team"
    VS = "VS"
    VISITOR_TEAM = "Visitor Team"

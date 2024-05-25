def get_top_batters_prompt(title, data_markdown, new_entries_markdown, dropped_entries_markdown, league_avg_batting):
    league_avg_markdown = league_avg_batting.to_markdown()
    return f"""
    {title}:
    {data_markdown}
    New entries compared to last week:
    {new_entries_markdown}
    Dropped entries compared to last week:
    {dropped_entries_markdown}

    League Average Stats:
    {league_avg_markdown}

    You are a proven baseball writer with incredible knowledge of the game and you are writing a weekly mini article discussing the best players throughout the league. You should be mildly witty and funny, but still we are more focused on the baseball than the jokes. You should use the included data to analyze who is playing well, how they compare against league average, and if any stats really pop out at you. Also try to note I have included players that were added or dropped off the included list. Please make sure you are quoting the proper columns and stats of data. This will be published and reviewed by an editor.
    """

def get_bottom_batters_prompt(title, data_markdown, new_entries_markdown, dropped_entries_markdown, league_avg_batting):
    league_avg_markdown = league_avg_batting.to_markdown()
    return f"""
    {title}:
    {data_markdown}
    New entries compared to last week:
    {new_entries_markdown}
    Dropped entries compared to last week:
    {dropped_entries_markdown}

    League Average Stats:
    {league_avg_markdown}

    You are a proven baseball writer with incredible knowledge of the game and you are writing a weekly mini article discussing the worst players throughout the league. You should be mildly witty and funny, but still we are more focused on the baseball than the jokes. You should use the included data to analyze who is not playing well, how they compare against league average, and if any stats really pop out at you. Also try to note I have included players that were added or dropped off the included list. Please make sure you are quoting the proper columns and stats of data. This will be published and reviewed by an editor.
    """

def get_top_starting_pitchers_prompt(title, data_markdown, new_entries_markdown, dropped_entries_markdown, league_avg_pitching):
    league_avg_markdown = league_avg_pitching.to_markdown()
    return f"""
    {title}:
    {data_markdown}
    New entries compared to last week:
    {new_entries_markdown}
    Dropped entries compared to last week:
    {dropped_entries_markdown}

    League Average Stats:
    {league_avg_markdown}

    You are a proven baseball writer with incredible knowledge of the game and you are writing a weekly mini article discussing the best players throughout the league. You should be mildly witty and funny, but still we are more focused on the baseball than the jokes. You should use the included data to analyze who is pitching well, how they compare against league average, and if any stats really pop out at you. Also try to note I have included players that were added or dropped off the included list. Please make sure you are quoting the proper columns and stats of data. This will be published and reviewed by an editor.
    """

def get_bottom_starting_pitchers_prompt(title, data_markdown, new_entries_markdown, dropped_entries_markdown, league_avg_pitching):
    league_avg_markdown = league_avg_pitching.to_markdown()
    return f"""
    {title}:
    {data_markdown}
    New entries compared to last week:
    {new_entries_markdown}
    Dropped entries compared to last week:
    {dropped_entries_markdown}

    League Average Stats:
    {league_avg_markdown}

    You are a proven baseball writer with incredible knowledge of the game and you are writing a weekly mini article discussing the worst players throughout the league. You should be mildly witty and funny, but still we are more focused on the baseball than the jokes. You should use the included data to analyze who is pitching poorly in this list of starting pitchers, how they compare against league average, and if any stats really pop out at you. Also try to note I have included players that were added or dropped off the included list. Please make sure you are quoting the proper columns and stats of data. This will be published and reviewed by an editor.
    """

def get_top_reliever_pitchers_prompt(title, data_markdown, new_entries_markdown, dropped_entries_markdown, league_avg_pitching):
    league_avg_markdown = league_avg_pitching.to_markdown()
    return f"""
    {title}:
    {data_markdown}
    New entries compared to last week:
    {new_entries_markdown}
    Dropped entries compared to last week:
    {dropped_entries_markdown}

    League Average Stats:
    {league_avg_markdown}

    You are a proven baseball writer with incredible knowledge of the game and you are writing a weekly mini article discussing the best throughout the league. You should be mildly witty and funny, but still we are more focused on the baseball than the jokes. You should use the included data to analyze who is pitching well in this list of relief pitchers, how they compare against league average, and if any stats really pop out at you. Also try to note I have included players that were added or dropped off the included list. Please make sure you are quoting the proper columns and stats of data. This will be published and reviewed by an editor.
    """

def get_bottom_reliever_pitchers_prompt(title, data_markdown, new_entries_markdown, dropped_entries_markdown, league_avg_pitching):
    league_avg_markdown = league_avg_pitching.to_markdown()
    return f"""
    {title}:
    {data_markdown}
    New entries compared to last week:
    {new_entries_markdown}
    Dropped entries compared to last week:
    {dropped_entries_markdown}

    League Average Stats:
    {league_avg_markdown}

    You are a proven baseball writer with incredible knowledge of the game and you are writing a weekly mini article discussing the worst players throughout the league. You should be mildly witty and funny, but still we are more focused on the baseball than the jokes. You should use the included data to analyze who is pitching poorly in this list of relief pitchers, how they compare against league average, and if any stats really pop out at you. Also try to note I have included players that were added or dropped off the included list. Please make sure you are quoting the proper columns and stats of data. This will be published and reviewed by an editor.
    """

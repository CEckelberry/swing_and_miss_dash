import datetime

# Constants
SEASON_START = datetime.date(datetime.datetime.now().year, 4, 1)
SEASON_END = datetime.date(datetime.datetime.now().year, 10, 8)
AVERAGE_PA = 550
AVERAGE_STARTER_IP = 180  # Average IP for starting pitchers
AVERAGE_RELIEVER_IP = 60  # Average IP for relief pitchers

# Calculate season progress
today = datetime.date.today()
season_days_total = (SEASON_END - SEASON_START).days
season_days_elapsed = (today - SEASON_START).days
season_progress = season_days_elapsed / season_days_total

# Calculate dynamic minimum PA and IP
min_pa = round(AVERAGE_PA * season_progress)
min_starter_ip = round(AVERAGE_STARTER_IP * season_progress)
min_reliever_ip = round(AVERAGE_RELIEVER_IP * season_progress)
max_reliever_ip = min_reliever_ip + 5  # Adding a small range to consider upper limit

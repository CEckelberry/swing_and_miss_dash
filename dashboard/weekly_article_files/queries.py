def get_top_starting_pitchers_query(season, min_starter_ip, start_date, end_date):
    return f"""
    WITH ranked_pitchers AS (
        SELECT 
            `Season`, `Name`, ROUND(`SIERA`, 2) AS `SIERA`, ROUND(`IP`, 1) AS `IP`, ROUND(`xFIP`, 2) AS `xFIP`, 
            `K_9` AS `K|9`, `FIP`, `GB_` AS `GB%`, `K_` AS `K%`, `BABIP`, `WAR`, `vFA__sc_` AS `vFA_sc`, `ERA`, 
            `BB_` AS `BB%`, `BB_9` AS `BB|9`, `SO`, `SwStr_` AS `SwStr%`, `LOB_` AS `LOB%`, `HR_FB` AS `HR|FB`, 
            `K_BB` AS `K|BB`, `WHIP`, `BB`, `Age`,
            ROW_NUMBER() OVER (PARTITION BY `Name` ORDER BY `SIERA` ASC) AS row_num
        FROM 
            `raw_data`.`pitching_stats`
        WHERE
            `Season` = {season} AND `IP` > {min_starter_ip} AND `upload_date` BETWEEN '{start_date}' AND '{end_date}'
    )
    SELECT * EXCEPT(row_num)
    FROM ranked_pitchers
    WHERE row_num = 1
    ORDER BY `SIERA` ASC
    LIMIT 10
    """

def get_bottom_starting_pitchers_query(season, min_starter_ip, start_date, end_date):
    return f"""
    WITH ranked_pitchers AS (
        SELECT 
            `Season`, `Name`, ROUND(`SIERA`, 2) AS `SIERA`, ROUND(`IP`, 1) AS `IP`, ROUND(`xFIP`, 2) AS `xFIP`, 
            `K_9` AS `K|9`, `FIP`, `GB_` AS `GB%`, `K_` AS `K%`, `BABIP`, `WAR`, `vFA__sc_` AS `vFA_sc`, `ERA`, 
            `BB_` AS `BB%`, `BB_9` AS `BB|9`, `SO`, `SwStr_` AS `SwStr%`, `LOB_` AS `LOB%`, `HR_FB` AS `HR|FB`, 
            `K_BB` AS `K|BB`, `WHIP`, `BB`, `Age`,
            ROW_NUMBER() OVER (PARTITION BY `Name` ORDER BY `SIERA` DESC) AS row_num
        FROM 
            `raw_data`.`pitching_stats`
        WHERE
            `Season` = {season} AND `IP` > {min_starter_ip} AND `upload_date` BETWEEN '{start_date}' AND '{end_date}'
    )
    SELECT * EXCEPT(row_num)
    FROM ranked_pitchers
    WHERE row_num = 1
    ORDER BY `SIERA` DESC
    LIMIT 10
    """

def get_top_reliever_pitchers_query(season, min_reliever_ip, max_reliever_ip, start_date, end_date):
    return f"""
    WITH ranked_relievers AS (
        SELECT 
            `Season`, `Name`, ROUND(`SIERA`, 2) AS `SIERA`, ROUND(`IP`, 1) AS `IP`, ROUND(`xFIP`, 2) AS `xFIP`, 
            `K_9` AS `K|9`, `FIP`, `GB_` AS `GB%`, `K_` AS `K%`, `BABIP`, `WAR`, `vFA__sc_` AS `vFA_sc`, `ERA`, 
            `BB_` AS `BB%`, `BB_9` AS `BB|9`, `SO`, `SwStr_` AS `SwStr%`, `LOB_` AS `LOB%`, `HR_FB` AS `HR|FB`, 
            `K_BB` AS `K|BB`, `WHIP`, `BB`, `Age`,
            ROW_NUMBER() OVER (PARTITION BY `Name` ORDER BY `SIERA` ASC) AS row_num
        FROM 
            `raw_data`.`pitching_stats`
        WHERE
            `Season` = {season} AND `IP` BETWEEN {min_reliever_ip} AND {max_reliever_ip} AND `upload_date` BETWEEN '{start_date}' AND '{end_date}'
    )
    SELECT * EXCEPT(row_num)
    FROM ranked_relievers
    WHERE row_num = 1
    ORDER BY `SIERA` ASC
    LIMIT 10
    """

def get_bottom_reliever_pitchers_query(season, min_reliever_ip, max_reliever_ip, start_date, end_date):
    return f"""
    WITH ranked_relievers AS (
        SELECT 
            `Season`, `Name`, ROUND(`SIERA`, 2) AS `SIERA`, ROUND(`IP`, 1) AS `IP`, ROUND(`xFIP`, 2) AS `xFIP`, 
            `K_9` AS `K|9`, `FIP`, `GB_` AS `GB%`, `K_` AS `K%`, `BABIP`, `WAR`, `vFA__sc_` AS `vFA_sc`, `ERA`, 
            `BB_` AS `BB%`, `BB_9` AS `BB|9`, `SO`, `SwStr_` AS `SwStr%`, `LOB_` AS `LOB%`, `HR_FB` AS `HR|FB`, 
            `K_BB` AS `K|BB`, `WHIP`, `BB`, `Age`,
            ROW_NUMBER() OVER (PARTITION BY `Name` ORDER BY `SIERA` DESC) AS row_num
        FROM 
            `raw_data`.`pitching_stats`
        WHERE
            `Season` = {season} AND `IP` BETWEEN {min_reliever_ip} AND {max_reliever_ip} AND `upload_date` BETWEEN '{start_date}' AND '{end_date}'
    )
    SELECT * EXCEPT(row_num)
    FROM ranked_relievers
    WHERE row_num = 1
    ORDER BY `SIERA` DESC
    LIMIT 10
    """

def get_top_batters_query(season, min_pa, start_date, end_date):
    return f"""
    WITH ranked_batters AS (
        SELECT 
            `Season`, `Name`, ROUND(`AVG`, 3) AS `AVG`, ROUND(`OBP`, 3) AS `OBP`, ROUND(`SLG`, 3) AS `SLG`, 
            `wRC_`, ROUND(`wOBA`, 3) AS `wOBA`, ROUND(`OPS`, 3) AS `OPS`, ROUND(`BABIP`, 3) AS `BABIP`, `WAR`, 
            `K_` AS `K%`, `BB_` AS `BB%`, `HR`, `Def`, `SB`, `CS`, `BsR`, `3B` AS `Triples`, `2B` AS `Doubles`, 
            `RBI`, `H` AS `Hits`, `Age`, `G`, `PA`,
            ROW_NUMBER() OVER (PARTITION BY `Name` ORDER BY `wRC_` DESC) AS row_num
        FROM 
            `raw_data`.`batting_stats`
        WHERE
            `Season` = {season} AND `PA` >= {min_pa} AND `upload_date` BETWEEN '{start_date}' AND '{end_date}'
    )
    SELECT 
        `Season`, `Name`, `AVG`, `OBP`, `SLG`, `wRC_` AS `wRC+`, `wOBA`, `OPS`, `BABIP`, `WAR`, `K%`, `BB%`, `HR`, `Def`, `SB`, `CS`, `BsR`,
        `Triples`, `Doubles`, `RBI`, `Hits`, `Age`, `G`, `PA`
    FROM ranked_batters
    WHERE row_num = 1
    ORDER BY `wRC+` DESC
    LIMIT 10
    """

def get_bottom_batters_query(season, min_pa, start_date, end_date):
    return f"""
    WITH ranked_batters AS (
        SELECT 
            `Season`, `Name`, ROUND(`AVG`, 3) AS `AVG`, ROUND(`OBP`, 3) AS `OBP`, ROUND(`SLG`, 3) AS `SLG`, 
            `wRC_`, ROUND(`wOBA`, 3) AS `wOBA`, ROUND(`OPS`, 3) AS `OPS`, ROUND(`BABIP`, 3) AS `BABIP`, `WAR`, 
            `K_` AS `K%`, `BB_` AS `BB%`, `HR`, `Def`, `SB`, `CS`, `BsR`, `3B` AS `Triples`, `2B` AS `Doubles`, 
            `RBI`, `H` AS `Hits`, `Age`, `G`, `PA`,
            ROW_NUMBER() OVER (PARTITION BY `Name` ORDER BY `wRC_` ASC) AS row_num
        FROM 
            `raw_data`.`batting_stats`
        WHERE
            `Season` = {season} AND `PA` >= {min_pa} AND `upload_date` BETWEEN '{start_date}' AND '{end_date}'
    )
    SELECT 
        `Season`, `Name`, `AVG`, `OBP`, `SLG`, `wRC_` AS `wRC+`, `wOBA`, `OPS`, `BABIP`, `WAR`, `K%`, `BB%`, `HR`, `Def`, `SB`, `CS`, `BsR`,
        `Triples`, `Doubles`, `RBI`, `Hits`, `Age`, `G`, `PA`
    FROM ranked_batters
    WHERE row_num = 1
    ORDER BY `wRC+` ASC
    LIMIT 10
    """

import pandas as pd
import numpy as np

pd.options.display.max_rows = 1000
pd.options.display.max_columns = 100


def read_stat(pattern, year):
    return pd.read_csv(r"data_{1}\{0}.csv".format(pattern, year)).drop(
        columns=["Referee", "HFKC", "AFKC", "Attendance", "HHW", "AHW", "Date"], errors="ignore").iloc[:, :6]


def make_match(data, home_team, away_team, tour_number, tour_length):
    home_win_at_home = 0
    home_match_at_home = 0
    away_win_away = 0
    away_match_away = 0
    home_points = 0
    away_points = 0
    home_points_last5 = 0
    away_points_last5 = 0
    home_scored = []
    home_skipped = []
    away_scored = []
    away_skipped = []

    for i in range(tour_number*tour_length):
        row = data.loc[i]
        if row[1] == home_team:
            home_scored.append(int(row[3]))
            home_skipped.append(int(row[4]))
            home_win_at_home += 1 if row[5] == "H" else 0
            home_match_at_home += 1
            home_points += 3 if row[5] == "H" else (1 if row[5] == "D" else 0)
        elif row[2] == home_team:
            home_scored.append(int(row[4]))
            home_skipped.append(int(row[3]))
            home_points += 3 if row[5] == "A" else (1 if row[5] == "D" else 0)
        else:
            pass

        if row[2] == away_team:
            away_scored.append(int(row[4]))
            away_skipped.append(int(row[3]))
            away_win_away += 1 if row[5] == "A" else 0
            away_match_away += 1
            away_points += 3 if row[5] == "A" else (1 if row[5] == "D" else 0)
        elif row[1] == away_team:
            away_scored.append(int(row[3]))
            away_skipped.append(int(row[4]))
            away_points += 3 if row[5] == "H" else (1 if row[5] == "D" else 0)
        else:
            pass

    field_factor = home_win_at_home/home_match_at_home - away_win_away/away_match_away \
        if home_match_at_home*away_match_away > 0 else 0

    if tour_number <= 5:
        return [home_points - away_points, home_points - away_points, field_factor,
                np.mean(home_scored), np.mean(home_skipped), np.mean(away_scored), np.mean(away_skipped)]

    else:
        for i in range((tour_number-4)*tour_length, tour_number*tour_length):
            row = data.loc[i]

            if row[1] == home_team:
                home_points_last5 += 3 if row[5] == "H" else (1 if row[5] == "D" else 0)
            elif row[2] == home_team:
                home_points_last5 += 3 if row[5] == "A" else (1 if row[5] == "D" else 0)
            else:
                pass

            if row[2] == away_team:
                away_points_last5 += 3 if row[5] == "A" else (1 if row[5] == "D" else 0)
            elif row[1] == away_team:
                away_points_last5 += 3 if row[5] == "H" else (1 if row[5] == "D" else 0)
            else:
                pass

        return [home_points - away_points, home_points_last5 - away_points_last5, field_factor,
                np.mean(home_scored), np.mean(home_skipped), np.mean(away_scored), np.mean(away_skipped)]


def score_interpreter(string):
    return 1 if string == "H" else (0 if string == "D" else -1)


def make_list_from_league(pattern, year):
    data = read_stat(pattern, year)
    tour_number = 1
    i = 0
    tour_length, list_length = (10, 380) if pattern in ["I1", "E0", "SP1", "F1"] else\
        ((9, 306) if pattern == "D1" else (12, 552))
    list_from_league = pd.DataFrame(columns=["HP-AP", "H5LP - A5LP", "FF",
                                             "MHScored", "MHSkipped", "MAScored", "MASkipped"],
                                    index=range(1, list_length+1))
    for row in data.itertuples():
        home_team = row[2]
        away_team = row[3]
        print(tour_number)
        i += 1
        list_from_league.loc[i] = make_match(data, home_team, away_team, tour_number, tour_length)
        if i % tour_length == 0:
            tour_number += 1
    list_from_league = list_from_league.reset_index().drop(columns=["index"])

    return list_from_league.assign(R=list(map(score_interpreter, data["FTR"].values)))


def make_training_set():
    data_set = make_list_from_league("I1", 2016)
    data_set = data_set.append(make_list_from_league("I1", 2015))
    data_set = data_set.append(make_list_from_league("I1", 2014))
    data_set = data_set.append(make_list_from_league("I1", 2013))
    data_set = data_set.append(make_list_from_league("I1", 2012))
    data_set = data_set.append(make_list_from_league("I1", 2011))
    data_set = data_set.append(make_list_from_league("I1", 2010))
    data_set = data_set.append(make_list_from_league("F1", 2016))
    data_set = data_set.append(make_list_from_league("F1", 2015))
    data_set = data_set.append(make_list_from_league("F1", 2014))
    data_set = data_set.append(make_list_from_league("F1", 2013))
    data_set = data_set.append(make_list_from_league("F1", 2012))
    data_set = data_set.append(make_list_from_league("F1", 2011))
    data_set = data_set.append(make_list_from_league("F1", 2010))
    data_set = data_set.append(make_list_from_league("E0", 2016))
    data_set = data_set.append(make_list_from_league("E0", 2015))
    data_set = data_set.append(make_list_from_league("E0", 2014))
    data_set = data_set.append(make_list_from_league("E0", 2013))
    data_set = data_set.append(make_list_from_league("E0", 2012))
    data_set = data_set.append(make_list_from_league("E0", 2011))
    data_set = data_set.append(make_list_from_league("E0", 2010))
    data_set = data_set.append(make_list_from_league("E1", 2016))
    data_set = data_set.append(make_list_from_league("E1", 2015))
    data_set = data_set.append(make_list_from_league("E1", 2014))
    data_set = data_set.append(make_list_from_league("E1", 2013))
    data_set = data_set.append(make_list_from_league("E1", 2012))
    data_set = data_set.append(make_list_from_league("E1", 2011))
    data_set = data_set.append(make_list_from_league("E1", 2010))
    data_set = data_set.append(make_list_from_league("D1", 2016))
    data_set = data_set.append(make_list_from_league("D1", 2015))
    data_set = data_set.append(make_list_from_league("D1", 2014))
    data_set = data_set.append(make_list_from_league("D1", 2013))
    data_set = data_set.append(make_list_from_league("D1", 2012))
    data_set = data_set.append(make_list_from_league("D1", 2011))
    data_set = data_set.append(make_list_from_league("D1", 2010))
    data_set = data_set.append(make_list_from_league("SP1", 2016))
    data_set = data_set.append(make_list_from_league("SP1", 2015))
    data_set = data_set.append(make_list_from_league("SP1", 2014))
    data_set = data_set.append(make_list_from_league("SP1", 2013))
    data_set = data_set.append(make_list_from_league("SP1", 2012))
    data_set = data_set.append(make_list_from_league("SP1", 2011))
    data_set = data_set.append(make_list_from_league("SP1", 2010))
    return data_set


def make_testing_set():
    data_set = make_list_from_league("I1", 2017)
    data_set = data_set.append(make_list_from_league("E0", 2017))
    data_set = data_set.append(make_list_from_league("E1", 2017))
    data_set = data_set.append(make_list_from_league("D1", 2017))
    data_set = data_set.append(make_list_from_league("F1", 2017))
    data_set = data_set.append(make_list_from_league("SP1", 2017))
    return data_set




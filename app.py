import json
import re
from flask import Flask, request
from pybaseball import batting_stats, cache
import sys

cache.enable()


def enforce_years(argument):
    pattern = re.compile("^([0-9]{4})(-[0-9]{4})?$")
    if pattern.match(argument):
        return argument
    else:
        raise ValueError(
            "You must either supply a single season, or multiple, consecutive"
            " seasons separated by a hyphen.\nEx. 2001-2004"
        )


# parser = argparse.ArgumentParser(
#     description=(
#         "A utility that pulls, graphs, and compares historical traditional and"
#         " expected stats in order to determine which is a better indicator of"
#         " future performance\nPearson's Correlation Coefficient will be used to judge which stat has a"
#         " strong, linear correlation to future production"
#     )
# )
# parser.add_argument(
#     "--sample_seasons",
#     help="The season(s) you want to use as a baseline",
#     type=enforce_years,
#     required=True,
# )
# parser.add_argument(
#     "--test_season",
#     help=(
#         "The future season you want to use to see if traditional stats or"
#         " expected stats are a better predictor of"
#     ),
#     type=int,
#     required=True,
# )

# args = parser.parse_args()
is_multiple_seasons = False
# if "-" in args.sample_seasons:
#     is_multiple_seasons = True
# first_year = (
#     args.sample_seasons
#     if "-" not in args.sample_seasons
#     else int(args.sample_seasons[0:4])
# )
# if int(first_year) < 2015:
#     print(
#         "ERROR: Statcast data was introduced in 2015, you cannot search for"
#         " data before this point\n"
#     )
#     sys.exit(1)


# def compute_expected_stat(player, stat):
#     denom = 0
#     sum_stat = 0
#     results_dict = {}
#     begin_year = (
#         int(args.sample_seasons[0:4])
#         if "-" in args.sample_seasons
#         else int(args.sample_seasons)
#     )
#     end_year = (
#         int(args.sample_seasons[5:9]) + 1
#         if "-" in args.sample_seasons
#         else int(args.sample_seasons) + 1
#     )
#     for year in range(begin_year, end_year):
#         if year == 2020:
#             continue
#         year_stats = batting_stats(year)
#         try:
#             exp_stat = year_stats.loc[year_stats["IDfg"] == player["IDfg"]][stat].item()
#         except Exception:
#             continue

#         if stat == "wOBA":
#             pas = year_stats.loc[year_stats["IDfg"] == player["IDfg"]]["PA"].item()
#             results_dict[year] = [pas, exp_stat]
#         else:
#             abs = year_stats.loc[year_stats["IDfg"] == player["IDfg"]]["AB"].item()
#             results_dict[year] = [abs, exp_stat]
#     denom = sum(val[0] for key, val in results_dict.items())
#     for key, val in results_dict.items():
#         pct = val[1]
#         opps = val[0]
#         sum_stat += (opps / denom) * pct
#     return sum_stat


# def build_comparison(player):
#     prev_BA = (
#         data_begin.loc[data_begin["IDfg"] == player["IDfg"]]["H"].item()
#         / data_begin.loc[data_begin["IDfg"] == player["IDfg"]]["AB"].item()
#     )
#     new_BA = (
#         data_end.loc[data_end["IDfg"] == player["IDfg"]]["H"].item()
#         / data_end.loc[data_end["IDfg"] == player["IDfg"]]["AB"].item()
#     )
#     prev_xBA = compute_expected_stat(player, "xBA")

#     prev_SLG = data_begin.loc[data_begin["IDfg"] == player["IDfg"]]["SLG"].item()
#     new_SLG = data_end.loc[data_end["IDfg"] == player["IDfg"]]["SLG"].item()
#     prev_xSLG = compute_expected_stat(player, "xSLG")

#     prev_wOBA = data_begin.loc[data_begin["IDfg"] == player["IDfg"]]["wOBA"].item()
#     new_wOBA = data_end.loc[data_end["IDfg"] == player["IDfg"]]["wOBA"].item()
#     prev_xwOBA = compute_expected_stat(player, "xwOBA")
#     name = data_begin.loc[data_begin["IDfg"] == player["IDfg"]]["Name"].item()
#     dct = {
#         "Name": name,
#         f"{args.sample_seasons} batting average": prev_BA,
#         f"{args.test_season} batting average": new_BA,
#         f"{args.sample_seasons} expected batting average": prev_xBA,
#         f"{args.sample_seasons} slugging %": prev_SLG,
#         f"{args.test_season} slugging %": new_SLG,
#         f"{args.sample_seasons} expected slugging %": prev_xSLG,
#         f"{args.sample_seasons} weighted on base average": prev_wOBA,
#         f"{args.test_season} weighted on base average": new_wOBA,
#         f"{args.sample_seasons} expected weighted on base average": prev_xwOBA,
#     }
#     if prev_xwOBA == 0:
#         dct = {}
#     return dct


# data_begin = (
#     batting_stats(args.sample_seasons, qual=502)
#     if not is_multiple_seasons
#     else batting_stats(
#         args.sample_seasons[0:4],
#         end_season=args.sample_seasons[5:9],
#         qual=502,
#         ind=0,
#     )
# )
# expected_cols = [col for col in data_begin if col.startswith("x")]
# actual_cols = [col[1:] for col in expected_cols]
# try:
#     data_end = batting_stats(args.test_season)
# except Exception:
#     print(
#         f"ERROR: Cannot fetch Statcast data for {args.test_season}. Has data"
#         " been published for this year yet?\n"
#     )
#     sys.exit(1)

# relevant_players = data_begin.loc[data_begin["IDfg"].isin(data_end["IDfg"])]

# player_dicts = []
# for index, row in relevant_players.iterrows():
#     dct = build_comparison(row)
#     if dct:
#         player_dicts.append(dct)


# df = pd.DataFrame(player_dicts)
# test_df = pd.concat(
#     [
#         df[f"{args.test_season} batting average"],
#         df[f"{args.sample_seasons} expected batting average"],
#     ],
#     axis=1,
# )
# test_df_a = pd.concat(
#     [
#         df[f"{args.test_season} batting average"],
#         df[f"{args.sample_seasons} batting average"],
#     ],
#     axis=1,
# )
# fig_ba, ax_ba = plt.subplots(1, 2, figsize=(10, 5))
# fig_ba.suptitle(
#     "Batting Average v. Expected Batting Average as indicator of future" " production"
# )
# fig_slg, ax_slg = plt.subplots(1, 2, figsize=(10, 5))
# fig_slg.suptitle("Slugging % v. Expected Slugging % as indicator of future production")
# fig_oba, ax_oba = plt.subplots(1, 2, figsize=(10, 5))
# fig_oba.suptitle(
#     "Weighted On Base Average v. Expected Weighted On Base Average as indicator"
#     " of future production"
# )
# sns.regplot(
#     df,
#     x=f"{args.sample_seasons} batting average",
#     y=f"{args.test_season} batting average",
#     fit_reg=True,
#     scatter=True,
#     ax=ax_ba[0],
# )
# ax_ba[0].set_title(
#     "Pearson coefficient:"
#     f" {str(round(pd.concat([df[f'{args.test_season} batting average'], df[f'{args.sample_seasons} batting average']], axis=1).corr().iloc[0,1],2))}"
# )
# sns.regplot(
#     df,
#     x=f"{args.sample_seasons} expected batting average",
#     y=f"{args.test_season} batting average",
#     fit_reg=True,
#     scatter=True,
#     ax=ax_ba[1],
# )
# ax_ba[1].set_title(
#     "Pearson coefficient:"
#     f" {str(round(pd.concat([df[f'{args.test_season} batting average'], df[f'{args.sample_seasons} expected batting average']], axis=1).corr().iloc[0,1],2))}"
# )
# sns.regplot(
#     df,
#     x=f"{args.sample_seasons} slugging %",
#     y=f"{args.test_season} slugging %",
#     fit_reg=True,
#     scatter=True,
#     ax=ax_slg[0],
# )
# ax_slg[0].set_title(
#     "Pearson coefficient:"
#     f" {str(round(pd.concat([df[f'{args.test_season} slugging %'], df[f'{args.sample_seasons} slugging %']], axis=1).corr().iloc[0,1],2))}"
# )
# sns.regplot(
#     df,
#     x=f"{args.sample_seasons} expected slugging %",
#     y=f"{args.test_season} slugging %",
#     fit_reg=True,
#     scatter=True,
#     ax=ax_slg[1],
# )
# ax_slg[1].set_title(
#     "Pearson coefficient:"
#     f" {str(round(pd.concat([df[f'{args.test_season} slugging %'], df[f'{args.sample_seasons} expected slugging %']], axis=1).corr().iloc[0,1],2))}"
# )
# sns.regplot(
#     df,
#     x=f"{args.sample_seasons} weighted on base average",
#     y=f"{args.test_season} weighted on base average",
#     fit_reg=True,
#     scatter=True,
#     ax=ax_oba[0],
# )
# ax_oba[0].set_title(
#     "Pearson coefficient:"
#     f" {str(round(pd.concat([df[f'{args.test_season} weighted on base average'], df[f'{args.sample_seasons} weighted on base average']], axis=1).corr().iloc[0,1],2))}"
# )
# sns.regplot(
#     df,
#     x=f"{args.sample_seasons} expected weighted on base average",
#     y=f"{args.test_season} weighted on base average",
#     fit_reg=True,
#     scatter=True,
#     ax=ax_oba[1],
# )
# ax_oba[1].set_title(
#     "Pearson coefficient:"
#     f" {str(round(pd.concat([df[f'{args.test_season} weighted on base average'], df[f'{args.sample_seasons} expected weighted on base average']], axis=1).corr().iloc[0,1],2))}"
# )
# plt.show(


app = Flask(__name__)
app.secret_key = "Necessary_to_have"
app.debug = True
app.config["DESTINATION_PASSWORD"] = "bulljive"


@app.route("/", methods=["GET"])
def get_stats():
    payload = request.get_json()
    try:
        player = payload["player"]
        year = payload["year"]
        stat = payload["stat"]

        year_stats = batting_stats(
            year,
            qual=100,
            ind=0,
        )
        output = year_stats.loc[year_stats["Name"] == player][stat].item()
        result = {"player": player, "stat": stat, "year": year, "value": output}

        return result
    except Exception:
        return {"result": "cannot find player/year/stat combo"}


# code goes here


if __name__ == "__main__":
    app.run()

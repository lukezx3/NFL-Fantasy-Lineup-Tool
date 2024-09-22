from espn_api.football import League
import os
from dotenv import load_dotenv

load_dotenv()
SWID = os.getenv("SWID")
ESPN_S2 = os.getenv("ESPN_S2")
LEAGUE_ID = os.getenv("LEAGUE_ID")

league = League(
    league_id=LEAGUE_ID,
    year=2024,
    swid=SWID,
    espn_s2=ESPN_S2
)

current_week = league.current_week

# Loop through each team in the league
for team in league.teams:
    roster = team.roster

    playerRosterDict = {}
    playerPointsDict = {}
    
    # Populate playerRosterDict and playerPointsDict for each player in the roster
    for player in roster:
        if player.position not in playerRosterDict:
            playerRosterDict[player.position] = [player]
        else:
            playerRosterDict[player.position].append(player)

        playerPointsDict[player.name] = player.stats[current_week]["projected_points"]

    # Start with an empty lineup
    best_lineup = {
        "QB": None,
        "RB": [],
        "WR": [],
        "TE": None,
        "Flex": None,
        "D/ST": None,
        "K": None,
    }

    # Sort players by position
    for key in playerRosterDict:
        # Sort players in each position by their projected points in descending order
        sorted_players = sorted(
            playerRosterDict[key],
            key=lambda player: playerPointsDict[player.name],
            reverse=True
        )
        
        # Process each position
        if key == "QB" and sorted_players:
            best_lineup["QB"] = sorted_players[0]  # Best QB
        
        elif key == "RB" and len(sorted_players) > 1:
            best_lineup["RB"] = sorted_players[:2]  # Top 2 RBs
        
        elif key == "WR" and len(sorted_players) > 1:
            best_lineup["WR"] = sorted_players[:2]  # Top 2 WRs
        
        elif key == "TE" and sorted_players:
            best_lineup["TE"] = sorted_players[0]  # Best TE

        elif key == "D/ST" and sorted_players:
            best_lineup["D/ST"] = sorted_players[0]  # Best D/ST

        elif key == "K" and sorted_players:
            best_lineup["K"] = sorted_players[0]  # Best Kicker

    # Flex consideration
    flex_candidates = []

    # Add remaining players for flex consideration
    if len(playerRosterDict.get("RB", [])) > 2:
        flex_candidates.extend(playerRosterDict["RB"][2:])  # Add RBs not in the top 2

    if len(playerRosterDict.get("WR", [])) > 2:
        flex_candidates.extend(playerRosterDict["WR"][2:])  # Add WRs not in the top 2

    if len(playerRosterDict.get("TE", [])) > 1:
        flex_candidates.append(playerRosterDict["TE"][1])  # Add TE if there's more than 1

    # Sort flex candidates by projected points
    flex_candidates = sorted(
        flex_candidates,
        key=lambda player: playerPointsDict[player.name],
        reverse=True
    )

    # Select the best Flex player (highest projected points)
    if flex_candidates:
        best_lineup["Flex"] = flex_candidates[0]

    # Display the best lineup for the current team
    print(f"\nBest Possible Starting Lineup for {team.team_name}")

    # Print QB
    qb = best_lineup["QB"]
    if qb:
        print(f"QB: {qb.name}, Projected Points: {playerPointsDict[qb.name]}")

    # Print RBs
    for i, rb in enumerate(best_lineup["RB"], 1):
        print(f"RB{i}: {rb.name}, Projected Points: {playerPointsDict[rb.name]}")

    # Print WRs
    for i, wr in enumerate(best_lineup["WR"], 1):
        print(f"WR{i}: {wr.name}, Projected Points: {playerPointsDict[wr.name]}")

    # Print TE
    te = best_lineup["TE"]
    if te:
        print(f"TE: {te.name}, Projected Points: {playerPointsDict[te.name]}")

    # Print Flex
    flex = best_lineup["Flex"]
    if flex:
        print(f"Flex: {flex.name}, Projected Points: {playerPointsDict[flex.name]}")

    # Print D/ST
    dst = best_lineup["D/ST"]
    if dst:
        print(f"D/ST: {dst.name}, Projected Points: {playerPointsDict[dst.name]}")

    # Print Kicker
    kicker = best_lineup["K"]
    if kicker:
        print(f"K: {kicker.name}, Projected Points: {playerPointsDict[kicker.name]}")
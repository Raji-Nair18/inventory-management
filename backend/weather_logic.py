def weather_multiplier(condition, category):
    if condition=="Rain" and category in ["snacks","umbrella"]:
        return 1.3
    if condition=="Summer" and category=="cold_drink":
        return 1.4
    if condition=="Winter" and category=="medicine":
        return 1.5
    return 1.0

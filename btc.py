from datetime import timedelta
import pandas as pd


def get_profitability(
    df, ndays=[5, 10, 15, 20, 25, 30], cutoff_margin=10, filter_date="2016-01-01"
):
    """
        This function takes in a dataframe containing daily open and close prices to estimate
        ROR after specified time periods from a given cut off date
            df : A dataframe containing daily open and close prices
            ndays : An arbitrary list of number of days that specify the intervals to estimate ROR
                        default = [5, 10, 15, 20, 25, 30]
            cutoff_margin : A candle in percentage points to identify a signal
                                default = 10
            filter_date :  All datapoints before this date are excluded

        Returns: Dataframe containing profitability estimates for every day we identify as a signal
        """
    df = df[df["Date"] > filter_date]
    df[">" + str(cutoff_margin) + "%"] = [
        True if abs(x) >= cutoff_margin else False for x in df["% delta"]
    ]
    pdf = df[df[">" + str(cutoff_margin) + "%"]]
    df.index = df["Date"]
    for n in ndays:
        pdf["%_" + str(n) + "_days"] = [
            (df.loc[date + timedelta(days=1)][1] - df.loc[date + timedelta(days=n)][2])
            / df.loc[date + timedelta(days=1)][1]
            for date in pdf["Date"]
        ]
    return df

# utils.py or views.py (wherever you want to place this logic)
from django.db.models import Max
import pandas as pd
from livedata.models import LiveFeedData
from .models import CandlestickPattern
from . import candle_functions

def fetch_latest_data():
    # Fetch the latest datetime from LiveFeedData
    latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
    
    if latest_datetime:
        data = LiveFeedData.objects.filter(datetime=latest_datetime).values(
            'symbol', 'open', 'high', 'low', 'ltp', 'volume', 'datetime'
        )
        return pd.DataFrame(list(data))
    else:
        print("No data found in the database.")
        return pd.DataFrame()

def detect_candlestick_patterns():
    df = fetch_latest_data()  # Get the latest data as a DataFrame

    if df.empty or len(df) < 3:
        print("Not enough data to detect patterns.")
        return  # Not enough data to detect patterns

    # Loop over the data and check for patterns
    for i in range(2, len(df)):  # Start at 2 to have 3 candles to compare
        candle1 = df.iloc[i - 2]
        candle2 = df.iloc[i - 1]
        candle3 = df.iloc[i]

        o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
        o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
        o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])

        # Check for Doji
        if candle_functions.is_doji(o1, c1, h1, l1) or candle_functions.is_doji(o2, c2, h2, l2) or candle_functions.is_doji(o3, c3, h3, l3):
            candlestick_pattern = "Doji"
        # Check for Two-Crow pattern
        elif candle_functions.is_two_crow(df, i):
            candlestick_pattern = "Two-Crow"
        elif candle_functions.is_three_black_crows(df,i):
            candlestick_pattern = "Three Black Crows"
        elif candle_functions.is_three_inside_up(df,i):
            candlestick_pattern = "3 Inside Up"
        elif candle_functions.is_hammer(o1, c1, h1, l1) or candle_functions.is_hammer(o2, c2, h2, l2) or candle_functions.is_hammer(o3, c3, h3, l3):
            candlestick_pattern = "Hammer"
        elif candle_functions.is_bullish_harami(df,i):
            candlestick_pattern = "Bullish Harami"
        elif candle_functions.is_bearish_harami(df,i):
            candlestick_pattern = "Bearish Harami"
        elif candle_functions.is_three_line_strike(df,i):
            candlestick_pattern = "3 Line Strike"
        elif candle_functions.is_three_outside_up(df,i):
            candlestick_pattern = "3 Outside Up"
        elif candle_functions.is_three_outside_down(df,i):
            candlestick_pattern = "3 Outside Down"
        elif candle_functions.is_three_stars_in_south(df,i):
            candlestick_pattern = "3 Stars In South"
        elif candle_functions.is_three_white_soldiers(df,i):
            candlestick_pattern = "3 White Soldiers"
        elif candle_functions.is_abandoned_baby(df,i):
            candlestick_pattern = "Abandoned Baby"
        elif candle_functions.is_advance_block(df,i):
            candlestick_pattern = "Advance Block"
        elif candle_functions.is_belthold(df,i):
            candlestick_pattern = "Belthold"
        elif candle_functions.is_breakaway(df,i):
            candlestick_pattern = "Breakaway"
        elif candle_functions.is_closing_marubozu(o1, c1, h1, l1) or candle_functions.is_closing_marubozu(o2, c2, h2, l2) or candle_functions.is_closing_marubozu(o3, c3, h3, l3):
            candlestick_pattern = "Closing Marubozu"
        elif candle_functions.is_conceal_baby_swallow(df,i):
            candlestick_pattern = "Conceal Baby Swallow"
        elif candle_functions.is_counterattack(df,i):
            candlestick_pattern = "CounterAttack"
        elif candle_functions.is_dark_cloud_cover(df,i):
            candlestick_pattern = "Dark Cloud Cover"
        elif candle_functions.is_doji_star(df,i):
            candlestick_pattern = "Doji Star"
        elif candle_functions.is_dragonfly_doji(o1, c1, h1, l1) or candle_functions.is_dragonfly_doji(o2, c2, h2, l2) or candle_functions.is_dragonfly_doji(o3, c3, h3, l3):
            candlestick_pattern = "Dragonfly Doji"
        elif candle_functions.is_bullish_engulfing(df,i):
            candlestick_pattern = "Bullish Engulfing"
        elif candle_functions.is_bearish_engulfing(df,i):
            candlestick_pattern = "Bearish Engulfing"
        elif candle_functions.is_evening_doji_star(df,i):
            candlestick_pattern = "Evening Doji Star"
        elif candle_functions.is_evening_star(df,i):
            candlestick_pattern = "Evening Star"
        elif candle_functions.is_gapside_side_white(df,i):
            candlestick_pattern = "Gapside Sidewhite"
        elif candle_functions.is_gravestone_doji(o1, c1, h1, l1) or candle_functions.is_gravestone_doji(o2, c2, h2, l2) or candle_functions.is_gravestone_doji(o3, c3, h3, l3):
            candlestick_pattern = "Gravestone Doji"
        elif candle_functions.is_hanging_man(o1, c1, h1, l1) or candle_functions.is_hanging_man(o2, c2, h2, l2) or candle_functions.is_hanging_man(o3, c3, h3, l3):
            candlestick_pattern = "Hanging Man"
        elif candle_functions.is_haramicross(df,i):
            candlestick_pattern = "HaramiCross"
        elif candle_functions.is_high_wave(o1, c1, h1, l1) or candle_functions.is_high_wave(o2, c2, h2, l2) or candle_functions.is_high_wave(o3, c3, h3, l3):
            candlestick_pattern = "High Wave"
        elif candle_functions.is_hikkake(df,i):
            candlestick_pattern = "Hikkake"
        elif candle_functions.is_hikkake_mod(df,i):
            candlestick_pattern = "Hikkake Mod"
        elif candle_functions.is_homing_pigeon(df,i):
            candlestick_pattern = "Homing Piegon"
        elif candle_functions.is_identical_three_crows(df,i):
            candlestick_pattern = "Identical 3 Crows"
        elif candle_functions.is_in_neck(df,i):
            candlestick_pattern = "Inneck"
        elif candle_functions.is_inside(df,i):
            candlestick_pattern = "Inside"
        elif candle_functions.is_inverted_hammer(o1, c1, h1, l1) or candle_functions.is_inverted_hammer(o2, c2, h2, l2) or candle_functions.is_inverted_hammer(o3, c3, h3, l3):
            candlestick_pattern = "Inverted Hammer"
        elif candle_functions.is_kicking_bullish(df,i):
            candlestick_pattern = "Kicking Bullish"
        elif candle_functions.is_kicking_bearish(df,i):
            candlestick_pattern = "Kicking Bearish"
        elif candle_functions.is_kicking_by_length(df,i):
            candlestick_pattern = "Kicking By Length"
        elif candle_functions.is_ladder_bottom(df,i):
            candlestick_pattern = "Ladder Bottom"
        elif candle_functions.is_long_legged_doji(o1, c1, h1, l1) or candle_functions.is_long_legged_doji(o2, c2, h2, l2) or candle_functions.is_long_legged_doji(o3, c3, h3, l3):
            candlestick_pattern = "Long Legged Doji"
        elif candle_functions.is_long_line(o1, c1, h1, l1) or candle_functions.is_long_line(o2, c2, h2, l2) or candle_functions.is_long_line(o3, c3, h3, l3):
            candlestick_pattern = "Long Line"
        elif candle_functions.is_marubozu(o1, c1, h1, l1) or candle_functions.is_marubozu(o2, c2, h2, l2) or candle_functions.is_marubozu(o3, c3, h3, l3):
            candlestick_pattern = "Marubozu"
        elif candle_functions.is_matching_low(df,i):
            candlestick_pattern = "Matching Low"
        elif candle_functions.is_mat_hold(df,i):
            candlestick_pattern = "Mat Hold"
        elif candle_functions.is_morning_doji_star(df,i):
            candlestick_pattern = "Morning Doji Star"
        elif candle_functions.is_morning_star(df,i):
            candlestick_pattern = "Morning Star"
        elif candle_functions.is_on_neck(df,i):
            candlestick_pattern = "On Neck"
        elif candle_functions.is_piercing_line(df,i):
            candlestick_pattern = "Piercing Line"
        elif candle_functions.is_rickshaw_man(o1, c1, h1, l1) or candle_functions.is_rickshaw_man(o2, c2, h2, l2) or candle_functions.is_rickshaw_man(o3, c3, h3, l3):
            candlestick_pattern = "Rickshaw Man"
        elif candle_functions.is_rise_fall_3_methods(df,i):
            candlestick_pattern = "Rise Fall 3 Methods"
        elif candle_functions.is_separating_lines(df,i):
            candlestick_pattern = "Separating Lines"
        elif candle_functions.is_shooting_star(o1, c1, h1, l1) or candle_functions.is_shooting_star(o2, c2, h2, l2) or candle_functions.is_shooting_star(o3, c3, h3, l3):
            candlestick_pattern = "Shooting Star"
        elif candle_functions.is_short_line(o1, c1, h1, l1) or candle_functions.is_short_line(o2, c2, h2, l2) or candle_functions.is_short_line(o3, c3, h3, l3):
            candlestick_pattern = "Short Line"
        elif candle_functions.is_spinning_top(o1, c1, h1, l1) or candle_functions.is_spinning_top(o2, c2, h2, l2) or candle_functions.is_spinning_top(o3, c3, h3, l3):
            candlestick_pattern = "Spining Top"
        elif candle_functions.is_stalled_pattern(df,i):
            candlestick_pattern = "Stalled Pattern"
        elif candle_functions.is_stick_sandwich(df,i):
            candlestick_pattern = "Sick Sandwich"
        elif candle_functions.is_takuri(o1, c1, h1, l1) or candle_functions.is_takuri(o2, c2, h2, l2) or candle_functions.is_takuri(o3, c3, h3, l3):
            candlestick_pattern = "Takuri"
        elif candle_functions.is_tasukigap(df,i):
            candlestick_pattern = "Tasukigap"
        elif candle_functions.is_thrusting(df,i):
            candlestick_pattern = "Thrusting"
        elif candle_functions.is_tri_star(df,i):
            candlestick_pattern = "Tri Star"
        elif candle_functions.is_unique_3_river(df,i):
            candlestick_pattern = "Unique 3 River"
        elif candle_functions.is_upside_gap_two_crows(df,i):
            candlestick_pattern = "Upside Gap 2 Crows"
        elif candle_functions.is_x_side_gap_three_methods(df,i):
            candlestick_pattern = "X Side Gap 3 Methods"

        else:
            candlestick_pattern = "No Pattern"

        # Save the result in CandlestickPattern model
        CandlestickPattern.objects.create(
            symbol=candle3['symbol'],
            date=candle3['datetime'].date(),
            time=candle3['datetime'].time(),
            candlestick_pattern=candlestick_pattern
        )

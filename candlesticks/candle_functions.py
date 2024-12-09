# utils.py (or any other appropriate file)
import pandas as pd
import numpy as np

# candle_functions.py
def is_doji(open_price, close_price, high_price, low_price, body_threshold=0.1):
    # Check for zero division
    if high_price == low_price:
        return False  # or handle this case differently if needed

    return abs(open_price - close_price) / (high_price - low_price) < body_threshold


def is_two_crow(df, index):
    if index < 2:
        return False
    
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    is_bullish_candle1 = o1 < c1
    is_small_body_candle2 = abs(o2 - c2) < (h2 - l2) * 0.3
    is_bearish_candle3 = o3 > c3
    is_candle3_closes_below_midpoint_candle1 = c3 < (o1 + c1) / 2
    is_candle3_closes_further_than_half = (c1 - c3) > (c1 - o1) * 0.5

    return (is_bullish_candle1 and
            is_small_body_candle2 and
            is_bearish_candle3 and
            is_candle3_closes_below_midpoint_candle1 and
            is_candle3_closes_further_than_half)

def is_three_black_crows(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    # Check if the pattern matches Three Black Crows criteria
    is_bearish_candle1 = o1 > c1
    is_bearish_candle2 = o2 > c2
    is_bearish_candle3 = o3 > c3
    opens_within_candle1 = o2 < c1 and o2 >= o1
    opens_within_candle2 = o3 < c2 and o3 >= o2
    closes_lower_than_previous_candle = c3 < c2 and c2 < c1
    
    return (is_bearish_candle1 and
            is_bearish_candle2 and
            is_bearish_candle3 and
            opens_within_candle1 and
            opens_within_candle2 and
            closes_lower_than_previous_candle)


def is_three_inside_up(df, index):
    if index < 2:
        return False
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    # Check if the pattern matches Three Inside Up criteria
    is_bearish_candle1 = o1 > c1
    is_bullish_candle2 = o2 < c2
    opens_within_candle1 = o2 > l1 and o2 < h1
    closes_within_candle1 = c2 > l1 and c2 < h1
    is_bullish_candle3 = o3 < c3
    closes_above_candle1_high = c3 > h1

    return (is_bearish_candle1 and
            is_bullish_candle2 and
            opens_within_candle1 and
            closes_within_candle1 and
            is_bullish_candle3 and
            closes_above_candle1_high)

def is_hammer(open_price, close_price, high_price, low_price, body_threshold=0.1, shadow_ratio=2):
    # Ensure that the high and low prices are not equal (to avoid zero division)
    candle_range = high_price - low_price
    if candle_range == 0:
        return False  # Return False if there's no range (flat candle)

    body_length = abs(open_price - close_price)
    lower_shadow_length = min(open_price, close_price) - low_price
    upper_shadow_length = high_price - max(open_price, close_price)
    
    # Check if the body is small relative to the total range
    is_small_body = body_length / candle_range < body_threshold
    # Check if the lower shadow is at least twice as long as the body
    is_long_lower_shadow = lower_shadow_length >= body_length * shadow_ratio
    # Check if the upper shadow is minimal
    is_small_upper_shadow = upper_shadow_length <= body_length * 0.1
    
    return is_small_body and is_long_lower_shadow and is_small_upper_shadow


def is_bullish_harami(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    
    # Check if the pattern matches Bullish Harami criteria
    is_bearish_candle1 = o1 > c1
    is_bullish_candle2 = o2 < c2
    is_candle2_within_candle1 = (l1 < l2 < h1) and (l1 < h2 < h1)
    
    return is_bearish_candle1 and is_bullish_candle2 and is_candle2_within_candle1

def is_bearish_harami(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    
    # Check if the pattern matches Bearish Harami criteria
    is_bullish_candle1 = o1 < c1
    is_bearish_candle2 = o2 > c2
    is_candle2_within_candle1 = (l1 < l2 < h1) and (l1 < h2 < h1)
    
    return is_bullish_candle1 and is_bearish_candle2 and is_candle2_within_candle1

def is_three_line_strike(df, index):
    if index < 3:
        return False
    
    # Get the four most recent candles
    candle1 = df.iloc[index - 3]
    candle2 = df.iloc[index - 2]
    candle3 = df.iloc[index - 1]
    candle4 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    o4, c4, h4, l4 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    # Check if the first three candles are of the same color
    all_bullish = o1 < c1 and o2 < c2 and o3 < c3
    all_bearish = o1 > c1 and o2 > c2 and o3 > c3
    
    # Check if the fourth candle completely engulfs the previous three
    if all_bullish:
        is_bullish_engulfing = o4 < min(o1, o2, o3) and c4 > max(c1, c2, c3)
    elif all_bearish:
        is_bearish_engulfing = o4 > max(o1, o2, o3) and c4 < min(c1, c2, c3)
    else:
        return False
    
    return (all_bullish and is_bullish_engulfing) or (all_bearish and is_bearish_engulfing)

def is_three_outside_up(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    # Check if the pattern matches Three Outside Up criteria
    is_bearish_candle1 = o1 > c1
    is_small_bullish_candle2 = o2 < c2 and l1 < l2 < h1 and l1 < h2 < h1
    is_bullish_candle3 = o3 < c3
    is_candle3_engulfing = o3 < min(o1, o2) and c3 > max(c1, c2)
    
    return (is_bearish_candle1 and
            is_small_bullish_candle2 and
            is_bullish_candle3 and
            is_candle3_engulfing)

def is_three_outside_down(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    # Check if the pattern matches Three Outside Down criteria
    is_bullish_candle1 = o1 < c1
    is_small_bearish_candle2 = o2 > c2 and l1 < l2 < h1 and l1 < h2 < h1
    is_bearish_candle3 = o3 > c3
    is_candle3_engulfing = o3 > max(o1, o2) and c3 < min(c1, c2)
    
    return (is_bullish_candle1 and
            is_small_bearish_candle2 and
            is_bearish_candle3 and
            is_candle3_engulfing)

def is_three_stars_in_south(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False  # Return False if the second candle has no range

    # Check if the pattern matches Three Stars in the South criteria
    is_bullish_candle1 = o1 < c1
    is_bearish_or_doji_candle2 = (o2 > c2) or (abs(o2 - c2) / (h2 - l2) < 0.1)
    is_candle2_within_candle1 = l1 < l2 < h1 and l1 < h2 < h1
    is_bearish_candle3 = o3 > c3
    is_candle3_closes_below_midpoint_candle1 = c3 < (o1 + c1) / 2
    
    return (is_bullish_candle1 and
            is_bearish_or_doji_candle2 and
            is_candle2_within_candle1 and
            is_bearish_candle3 and
            is_candle3_closes_below_midpoint_candle1)

def is_three_white_soldiers(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    # Check if the pattern matches Three White Soldiers criteria
    is_bullish_candle1 = o1 < c1
    is_bullish_candle2 = o2 < c2
    is_bullish_candle3 = o3 < c3
    
    # Check if each candle opens within the body of the previous candle
    opens_within_candle1 = o2 >= o1 and o2 < c1
    opens_within_candle2 = o3 >= o2 and o3 < c2
    
    # Check if each candle closes higher than the previous candle
    closes_higher_than_previous = c2 > c1 and c3 > c2
    
    return (is_bullish_candle1 and
            is_bullish_candle2 and
            is_bullish_candle3 and
            opens_within_candle1 and
            opens_within_candle2 and
            closes_higher_than_previous)

def is_abandoned_baby(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False  # Return False if the second candle has no range
    # Check if the pattern matches Abandoned Baby criteria
    is_bullish_candle1 = o1 < c1
    is_doji_candle2 = abs(o2 - c2) / (h2 - l2) < 0.1
    is_gapped_up = o2 > c1 and l2 > c1
    is_bearish_candle3 = o3 > c3
    is_candle3_opens_below_doji = o3 < c2
    is_candle3_closes_below_first_candle = c3 < l1
    
    return (is_bullish_candle1 and
            is_doji_candle2 and
            is_gapped_up and
            is_bearish_candle3 and
            is_candle3_opens_below_doji and
            is_candle3_closes_below_first_candle)

def is_advance_block(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    # Check if the pattern matches Advance Block criteria
    is_bullish_candle1 = o1 < c1
    is_bullish_candle2 = o2 < c2
    is_bearish_candle3 = o3 > c3
    
    # Check if the second candle opens within the body of the first candle and closes lower
    opens_within_candle1 = o2 >= o1 and o2 < c1
    closes_lower_than_candle1 = c2 < o1 and c2 < c1
    
    # Check if the third candle opens within the body of the second candle and closes below the low of the second candle
    opens_within_candle2 = o3 >= o2 and o3 < c2
    closes_below_candle2 = c3 < l2
    
    return (is_bullish_candle1 and
            is_bullish_candle2 and
            is_bearish_candle3 and
            opens_within_candle1 and
            closes_lower_than_candle1 and
            opens_within_candle2 and
            closes_below_candle2)


def is_belthold(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])

    
    # Check if the pattern matches Belthold criteria
    is_bullish_candle1 = o1 < c1
    is_bearish_candle2 = o2 > c2
    opens_at_or_above_candle1_high = o2 >= h1
    closes_lower_than_candle2_open = c2 < o2
    
    return (is_bullish_candle1 and
            is_bearish_candle2 and
            opens_at_or_above_candle1_high and
            closes_lower_than_candle2_open)


def is_breakaway(df, index):
    if index < 4:
        return False
    
    # Get the five most recent candles
    candle1 = df.iloc[index - 4]
    candle2 = df.iloc[index - 3]
    candle3 = df.iloc[index - 2]
    candle4 = df.iloc[index - 1]
    candle5 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    o4, c4, h4, l4 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o5, c5, h5, l5 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])

    candle2_range = h2 - l2
    if candle2_range == 0:
        return False  # Return False if the second candle has no range
    
    # Check if the pattern matches Breakaway criteria
    is_bullish_candle1 = o1 < c1
    is_small_candle2 = abs(o2 - c2) / (h2 - l2) < 0.3
    gaps_up_candle2 = o2 > c1
    is_bearish_candle3 = o3 > c3
    opens_at_or_above_candle2_high = o3 >= h2
    closes_below_midpoint_candle1 = c3 < (o1 + c1) / 2
    is_bearish_candle4 = o4 > c4
    closes_lower_than_candle3 = c4 < c3
    is_bearish_candle5 = o5 > c5
    closes_below_candle3_low = c5 < l3
    
    return (is_bullish_candle1 and
            is_small_candle2 and
            gaps_up_candle2 and
            is_bearish_candle3 and
            opens_at_or_above_candle2_high and
            closes_below_midpoint_candle1 and
            is_bearish_candle4 and
            closes_lower_than_candle3 and
            is_bearish_candle5 and
            closes_below_candle3_low)

def is_closing_marubozu(open_price, close_price, high_price, low_price, body_threshold=0.1, shadow_threshold=0.05):
    body_length = abs(open_price - close_price)
    if high_price == low_price:
        return False 
    candle_range = high_price - low_price
    upper_shadow_length = high_price - max(open_price, close_price)
    lower_shadow_length = min(open_price, close_price) - low_price
    
    # Check if the body is large relative to the candle range
    is_large_body = body_length / candle_range > body_threshold
    # Check if the upper and lower shadows are minimal
    is_small_upper_shadow = upper_shadow_length <= shadow_threshold * body_length
    is_small_lower_shadow = lower_shadow_length <= shadow_threshold * body_length
    
    return is_large_body and is_small_upper_shadow and is_small_lower_shadow


def is_conceal_baby_swallow(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    # Check if the pattern matches Conceal Baby Swallow criteria
    is_bullish_candle1 = o1 < c1
    is_small_body_candle2 = abs(o2 - c2) / (h2 - l2) < 0.3
    gaps_up_candle2 = o2 > c1
    is_bearish_candle3 = o3 > c3
    opens_at_or_above_candle2_high = o3 >= h2
    closes_below_candle1_low = c3 < l1

    return (is_bullish_candle1 and
            is_small_body_candle2 and
            gaps_up_candle2 and
            is_bearish_candle3 and
            opens_at_or_above_candle2_high and
            closes_below_candle1_low)

def is_counterattack(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    # Check if the pattern matches Counterattack criteria
    is_bullish_candle1 = o1 < c1
    is_bearish_candle2 = o2 > c2
    opens_at_or_above_candle1_high = o2 >= h1
    closes_near_candle1_open = abs(c2 - o1) <= abs(c1 - o1) * 0.3
    
    return (is_bullish_candle1 and
            is_bearish_candle2 and
            opens_at_or_above_candle1_high and
            closes_near_candle1_open)

def is_dark_cloud_cover(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])

    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    
    # Check if the pattern matches Dark Cloud Cover criteria
    is_bullish_candle1 = o1 < c1
    is_bearish_candle2 = o2 > c2
    opens_above_candle1_high = o2 > h1
    closes_below_midpoint_candle1 = c2 < (o1 + c1) / 2
    
    return (is_bullish_candle1 and
            is_bearish_candle2 and
            opens_above_candle1_high and
            closes_below_midpoint_candle1)

def is_doji_star(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])

    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    
    # Check if the pattern matches Doji Star criteria
    is_bullish_candle1 = o1 < c1
    is_doji_candle2 = abs(o2 - c2) / (h2 - l2) < 0.1  # Small body relative to the range
    opens_above_candle1_high = o2 > h1
    closes_near_candle2_open = abs(c2 - o2) < (h2 - l2) * 0.1  # Close near open

    return (is_bullish_candle1 and
            is_doji_candle2 and
            opens_above_candle1_high and
            closes_near_candle2_open)

def is_dragonfly_doji(open_price, close_price, high_price, low_price, body_threshold=0.1, shadow_ratio=2):
    body_length = abs(open_price - close_price)
    if high_price == low_price:
        return False 
    candle_range = high_price - low_price
    lower_shadow_length = open_price - low_price
    upper_shadow_length = high_price - max(open_price, close_price)
    
    # Check if the body is small relative to the total range
    is_small_body = body_length / candle_range < body_threshold
    # Check if the lower shadow is at least twice as long as the body
    is_long_lower_shadow = lower_shadow_length >= body_length * shadow_ratio
    # Check if the upper shadow is minimal
    is_small_upper_shadow = upper_shadow_length <= body_length * 0.1
    
    return is_small_body and is_long_lower_shadow and is_small_upper_shadow

def is_bullish_engulfing(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])

    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    
    # Check if the pattern matches Bullish Engulfing criteria
    is_bearish_candle1 = o1 > c1
    is_bullish_candle2 = o2 < c2
    engulfs_previous_body = o2 < c1 and c2 > o1
    
    return is_bearish_candle1 and is_bullish_candle2 and engulfs_previous_body

def is_bearish_engulfing(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])

    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    
    # Check if the pattern matches Bearish Engulfing criteria
    is_bullish_candle1 = o1 < c1
    is_bearish_candle2 = o2 > c2
    engulfs_previous_body = o2 > c1 and c2 < o1
    
    return is_bullish_candle1 and is_bearish_candle2 and engulfs_previous_body

def is_evening_doji_star(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    
    # Check if the pattern matches Evening Doji Star criteria
    is_bullish_candle1 = o1 < c1
    is_doji_candle2 = abs(o2 - c2) / (h2 - l2) < 0.1 and abs(o2 - c2) / (h2 - l2) < 0.1
    is_bearish_candle3 = o3 > c3
    is_candle3_closes_below_midpoint_candle1 = c3 < (o1 + c1) / 2
    
    return (is_bullish_candle1 and
            is_doji_candle2 and
            is_bearish_candle3 and
            is_candle3_closes_below_midpoint_candle1)

def is_evening_star(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    # Check if the pattern matches Evening Star criteria
    is_bullish_candle1 = o1 < c1
    is_small_body_candle2 = abs(o2 - c2) / (h2 - l2) < 0.3
    is_bearish_candle3 = o3 > c3
    is_candle3_closes_below_midpoint_candle1 = c3 < (o1 + c1) / 2
    
    return (is_bullish_candle1 and
            is_small_body_candle2 and
            is_bearish_candle3 and
            is_candle3_closes_below_midpoint_candle1)

def is_gapside_side_white(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    
    # Check if the pattern matches Gapside-Side-White criteria
    is_bullish_candle1 = o1 < c1
    is_small_bullish_candle2 = abs(o2 - c2) < (h2 - l2) * 0.3 and o2 > c1
    is_bullish_candle3 = o3 < c3
    is_candle3_opens_above_candle2_close = o3 > c2
    is_candle3_closes_above_candle2_open = c3 > o2

    return (is_bullish_candle1 and
            is_small_bullish_candle2 and
            is_bullish_candle3 and
            is_candle3_opens_above_candle2_close and
            is_candle3_closes_above_candle2_open)

def is_gravestone_doji(open_price, close_price, high_price, low_price, body_threshold=0.1, shadow_ratio=2):
    body_length = abs(open_price - close_price)
    if high_price == low_price:
        return False 
    candle_range = high_price - low_price
    upper_shadow_length = high_price - max(open_price, close_price)
    lower_shadow_length = min(open_price, close_price) - low_price
    
    # Check if the body is very small or non-existent
    is_small_body = body_length / candle_range < body_threshold
    # Check if the upper shadow is at least twice as long as the body
    is_long_upper_shadow = upper_shadow_length >= body_length * shadow_ratio
    # Check if there is minimal to no lower shadow
    is_small_lower_shadow = lower_shadow_length <= body_length * 0.1
    
    return is_small_body and is_long_upper_shadow and is_small_lower_shadow

def is_hanging_man(open_price, close_price, high_price, low_price, body_threshold=0.1, shadow_ratio=2):
    body_length = abs(open_price - close_price)
    if high_price == low_price:
        return False 
    candle_range = high_price - low_price
    lower_shadow_length = min(open_price, close_price) - low_price
    upper_shadow_length = high_price - max(open_price, close_price)
    
    # Check if the body is small relative to the total range
    is_small_body = body_length / candle_range < body_threshold
    # Check if the lower shadow is at least twice as long as the body
    is_long_lower_shadow = lower_shadow_length >= body_length * shadow_ratio
    # Check if the upper shadow is minimal
    is_small_upper_shadow = upper_shadow_length <= body_length * 0.1
    
    return is_small_body and is_long_lower_shadow and is_small_upper_shadow

def is_haramicross(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    
    # Check if the second candle is a Doji
    is_doji_candle2 = is_doji(o2, c2, h2, l2)
    
    if not is_doji_candle2:
        return False
    
    # Check if the first candle is bullish or bearish and the Doji is within its body
    is_bullish_candle1 = o1 < c1
    is_bearish_candle1 = o1 > c1
    is_candle2_within_candle1 = (l1 < l2 < h1) and (l1 < h2 < h1)
    
    return (is_bullish_candle1 or is_bearish_candle1) and is_candle2_within_candle1


def is_high_wave(open_price, close_price, high_price, low_price, body_threshold=0.1, shadow_ratio=2):
    body_length = abs(open_price - close_price)
    if high_price == low_price:
        return False 
    candle_range = high_price - low_price
    lower_shadow_length = min(open_price, close_price) - low_price
    upper_shadow_length = high_price - max(open_price, close_price)
    
    # Check if the body is small relative to the total range
    is_small_body = body_length / candle_range < body_threshold
    # Check if both shadows are at least twice as long as the body
    is_long_shadows = lower_shadow_length >= body_length * shadow_ratio and upper_shadow_length >= body_length * shadow_ratio
    
    return is_small_body and is_long_shadows

def is_hikkake(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    # Check if the pattern matches Hikkake criteria
    is_small_range_candle1 = (h1 - l1) < (h2 - l2) and (h1 - l1) < (h3 - l3)
    is_second_candle_follows_first = (o2 < c1 and c2 < c1) or (o2 > c1 and c2 > c1)
    is_reversal_in_candle3 = (o3 < c1 and c3 > c1) or (o3 > c1 and c3 < c1)
    
    return is_small_range_candle1 and is_second_candle_follows_first and is_reversal_in_candle3


def is_hikkake_mod(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    # Check if the pattern matches Hikkake Mod criteria
    is_small_range_candle1 = (h1 - l1) < (h2 - l2) and (h1 - l1) < (h3 - l3)
    is_second_candle_within_first_range = (l1 <= o2 <= h1) and (l1 <= c2 <= h1)
    is_reversal_in_candle3 = (o3 < l1 and c3 > h1) or (o3 > h1 and c3 < l1)
    
    return is_small_range_candle1 and is_second_candle_within_first_range and is_reversal_in_candle3


def is_homing_pigeon(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    # Check if the pattern matches Homing Pigeon criteria
    is_large_bearish_candle1 = o1 > c1 and (h1 - l1) > 2 * (c1 - o1)
    is_small_body_candle2 = abs(o2 - c2) < (h1 - l1) * 0.2
    is_candle2_within_first_candle_range = (l1 <= o2 <= h1) and (l1 <= c2 <= h1)
    is_large_bullish_candle3 = o3 < c3 and (h3 - l3) > 2 * (o3 - c3)
    is_candle3_closes_above_midpoint = c3 > (o1 + c1) / 2
    
    return (is_large_bearish_candle1 and
            is_small_body_candle2 and
            is_candle2_within_first_candle_range and
            is_large_bullish_candle3 and
            is_candle3_closes_above_midpoint)


def is_identical_three_crows(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    # Check if the pattern matches Identical Three Crows criteria
    is_bearish_candle1 = o1 > c1
    is_bearish_candle2 = o2 > c2
    is_bearish_candle3 = o3 > c3
    
    # Candles 2 and 3 should open within the body of the previous candle
    opens_within_candle1_body = (o2 >= c1 and o2 <= o1) and (o3 >= c2 and o3 <= o1)
    closes_within_candle1_body = (c2 >= c1 and c2 <= o1) and (c3 >= c2 and c3 <= o1)
    
    return (is_bearish_candle1 and
            is_bearish_candle2 and
            is_bearish_candle3 and
            opens_within_candle1_body and
            closes_within_candle1_body)

def is_in_neck(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    # Check if the pattern matches In-Neck criteria
    is_bullish_candle1 = o1 < c1
    is_bearish_candle2 = o2 > c2
    opens_within_body_candle1 = o2 > c1 and o2 < o1
    closes_below_candle1_close = c2 < c1
    not_below_candle1_midpoint = c2 > (o1 + c1) / 2

    return (is_bullish_candle1 and
            is_bearish_candle2 and
            opens_within_body_candle1 and
            closes_below_candle1_close and
            not_below_candle1_midpoint)


def is_inside(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    # Check if the pattern matches Inside criteria
    is_candle2_inside_candle1 = (l1 < l2 < h1) and (l1 < h2 < h1)

    return is_candle2_inside_candle1


def is_inverted_hammer(open_price, close_price, high_price, low_price, body_threshold=0.1, shadow_ratio=2):
    body_length = abs(open_price - close_price)
    if high_price == low_price:
        return False 
    candle_range = high_price - low_price
    lower_shadow_length = min(open_price, close_price) - low_price
    upper_shadow_length = high_price - max(open_price, close_price)
    
    # Check if the body is small relative to the total range
    is_small_body = body_length / candle_range < body_threshold
    # Check if the upper shadow is at least twice as long as the body
    is_long_upper_shadow = upper_shadow_length >= body_length * shadow_ratio
    # Check if the lower shadow is minimal
    is_small_lower_shadow = lower_shadow_length <= body_length * 0.1
    
    return is_small_body and is_long_upper_shadow and is_small_lower_shadow

def is_kicking_bullish(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    # Check if the pattern matches Kicking Bullish criteria
    is_bullish_candle1 = o1 < c1
    is_bullish_candle2 = o2 > c2
    is_gap_up = o2 > c1
    is_candle1_strong = c1 > o1 + (h1 - l1) * 0.3
    is_candle2_strong = c2 < o2 - (h2 - l2) * 0.3
    
    return (is_bullish_candle1 and
            is_bullish_candle2 and
            is_gap_up and
            is_candle1_strong and
            is_candle2_strong)

def is_kicking_bearish(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    # Check if the pattern matches Kicking Bearish criteria
    is_bearish_candle1 = o1 > c1
    is_bearish_candle2 = o2 < c2
    is_gap_down = o2 < c1
    is_candle1_strong = o1 > c1 + (h1 - l1) * 0.3
    is_candle2_strong = c2 > o2 + (h2 - l2) * 0.3
    
    return (is_bearish_candle1 and
            is_bearish_candle2 and
            is_gap_down and
            is_candle1_strong and
            is_candle2_strong)

def is_kicking_by_length(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    # Check if the pattern matches Kicking by Length criteria
    is_bullish_candle1 = o1 < c1
    is_bullish_candle2 = o2 > c2
    is_gap_up = o2 > c1
    is_candle1_longer = (c1 - o1) > (h2 - l2) * 1.5
    is_candle2_strong = (o2 - c2) > (h2 - l2) * 0.5
    
    return (is_bullish_candle1 and
            is_bullish_candle2 and
            is_gap_up and
            is_candle1_longer and
            is_candle2_strong)


def is_ladder_bottom(df, index):
    if index < 4:
        return False
    
    # Get the five most recent candles
    candle1 = df.iloc[index - 4]
    candle2 = df.iloc[index - 3]
    candle3 = df.iloc[index - 2]
    candle4 = df.iloc[index - 1]
    candle5 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    o4, c4, h4, l4 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o5, c5, h5, l5 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    
    # Check if the pattern matches Ladder Bottom criteria
    is_bearish_candle1 = o1 > c1
    is_bearish_candle2 = o2 > c2 and c2 >= o2
    is_bullish_candle3 = o3 < c3 and o3 > l2 and c3 < h2
    is_bullish_candle4 = o4 < c4 and c4 > c3
    is_bullish_candle5 = o5 < c5 and c5 > h4
    
    return (is_bearish_candle1 and
            is_bearish_candle2 and
            is_bullish_candle3 and
            is_bullish_candle4 and
            is_bullish_candle5)


def is_long_legged_doji(open_price, close_price, high_price, low_price, body_threshold=0.1, shadow_ratio=2):
    body_length = abs(open_price - close_price)
    if high_price == low_price:
        return False 
    candle_range = high_price - low_price
    lower_shadow_length = min(open_price, close_price) - low_price
    upper_shadow_length = high_price - max(open_price, close_price)
    
    # Check if the body is very small relative to the total range
    is_small_body = body_length / candle_range < body_threshold
    # Check if both shadows are at least twice as long as the body
    is_long_lower_shadow = lower_shadow_length >= body_length * shadow_ratio
    is_long_upper_shadow = upper_shadow_length >= body_length * shadow_ratio
    
    return is_small_body and is_long_lower_shadow and is_long_upper_shadow

def is_long_line(open_price, close_price, high_price, low_price, body_threshold=0.8):
    body_length = abs(open_price - close_price)
    if high_price == low_price:
        return False 
    candle_range = high_price - low_price
    
    # Check if the body is very long relative to the total range
    is_long_body = body_length / candle_range > body_threshold
    # Check if both shadows are minimal
    lower_shadow_length = min(open_price, close_price) - low_price
    upper_shadow_length = high_price - max(open_price, close_price)
    has_small_shadows = lower_shadow_length < body_length * 0.2 and upper_shadow_length < body_length * 0.2
    
    return is_long_body and has_small_shadows

def is_marubozu(open_price, close_price, high_price, low_price, shadow_threshold=0.1):
    body_length = abs(open_price - close_price)
    if high_price == low_price:
        return False 
    candle_range = high_price - low_price
    
    # Check if there are minimal shadows
    lower_shadow_length = min(open_price, close_price) - low_price
    upper_shadow_length = high_price - max(open_price, close_price)
    
    # For a bullish Marubozu: open is at low, close is at high
    is_bullish_marubozu = (open_price == low_price and close_price == high_price and
                           lower_shadow_length <= body_length * shadow_threshold and
                           upper_shadow_length <= body_length * shadow_threshold)
    
    # For a bearish Marubozu: open is at high, close is at low
    is_bearish_marubozu = (open_price == high_price and close_price == low_price and
                           lower_shadow_length <= body_length * shadow_threshold and
                           upper_shadow_length <= body_length * shadow_threshold)
    
    return is_bullish_marubozu or is_bearish_marubozu

def is_matching_low(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False
    # Check if the pattern matches Matching Low criteria
    is_bearish_candle1 = o1 > c1
    is_bullish_candle2 = o2 < c2
    has_matching_low = l1 == l2
    
    return is_bearish_candle1 and is_bullish_candle2 and has_matching_low


def is_mat_hold(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False  # Return False if the second candle has no range

    # Check if the pattern matches Mat Hold criteria
    is_bullish_candle1 = o1 < c1
    is_small_body_candle2 = abs(o2 - c2) < (h2 - l2) * 0.3
    is_candle2_within_candle1 = (l1 < l2 < h1) and (l1 < h2 < h1)
    is_bullish_candle3 = o3 < c3
    is_candle3_closes_above_candle1_high = c3 > h1
    
    return (is_bullish_candle1 and
            is_small_body_candle2 and
            is_candle2_within_candle1 and
            is_bullish_candle3 and
            is_candle3_closes_above_candle1_high)


def is_morning_doji_star(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False  # Return False if the second candle has no range

    # Check if the pattern matches Morning Doji Star criteria
    is_bearish_candle1 = o1 > c1
    is_doji_candle2 = abs(o2 - c2) / (h2 - l2) < 0.1
    is_candle2_gaps_down = o2 < c1 and c2 < l1
    is_bullish_candle3 = o3 < c3
    is_candle3_closes_above_midpoint_candle1 = c3 > (o1 + c1) / 2
    
    return (is_bearish_candle1 and
            is_doji_candle2 and
            is_candle2_gaps_down and
            is_bullish_candle3 and
            is_candle3_closes_above_midpoint_candle1)

def is_morning_star(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False  # Return False if the second candle has no range

    # Check if the pattern matches Morning Star criteria
    is_bearish_candle1 = o1 > c1
    is_small_body_candle2 = abs(o2 - c2) / (h2 - l2) < 0.3
    is_candle2_gaps_down = o2 < c1 and c2 < l1
    is_bullish_candle3 = o3 < c3
    is_candle3_closes_into_body_candle1 = c3 > (o1 + c1) / 2
    
    return (is_bearish_candle1 and
            is_small_body_candle2 and
            is_candle2_gaps_down and
            is_bullish_candle3 and
            is_candle3_closes_into_body_candle1)

def is_on_neck(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False  # Return False if the second candle has no range

    # Check if the pattern matches On-Neck criteria
    is_bearish_candle1 = o1 > c1
    is_bullish_candle2 = o2 < c2
    is_candle2_opens_below_candle1 = o2 < l1
    is_candle2_closes_at_or_above_candle1_close = c2 >= c1
    
    return (is_bearish_candle1 and
            is_bullish_candle2 and
            is_candle2_opens_below_candle1 and
            is_candle2_closes_at_or_above_candle1_close)

def is_piercing_line(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False  # Return False if the second candle has no range

    # Check if the pattern matches Piercing Line criteria
    is_bearish_candle1 = o1 > c1
    is_bullish_candle2 = o2 < c2
    is_candle2_opens_below_candle1_low = o2 < l1
    is_candle2_closes_above_midpoint = c2 > (o1 + c1) / 2
    
    return (is_bearish_candle1 and
            is_bullish_candle2 and
            is_candle2_opens_below_candle1_low and
            is_candle2_closes_above_midpoint)

def is_rickshaw_man(open_price, close_price, high_price, low_price):
    body_length = abs(open_price - close_price)
    if high_price == low_price:
        return False 
    candle_range = high_price - low_price
    upper_shadow = high_price - max(open_price, close_price)
    lower_shadow = min(open_price, close_price) - low_price
    
    # Rickshaw Man criteria: small body with long upper and lower shadows
    is_small_body = body_length <= 0.2 * candle_range
    is_long_upper_shadow = upper_shadow >= 2 * body_length
    is_long_lower_shadow = lower_shadow >= 2 * body_length
    
    return is_small_body and is_long_upper_shadow and is_long_lower_shadow


def is_rise_fall_3_methods(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False  # Return False if the second candle has no range

    # Check if the pattern matches Rise-Fall 3 Methods criteria
    is_bullish_candle1 = o1 < c1
    is_candle2_within_candle1 = (l1 < l2 < h1) and (l1 < h2 < h1)
    is_bullish_candle3 = o3 < c3
    closes_above_candle1_close = c3 > c1
    
    return (is_bullish_candle1 and
            is_candle2_within_candle1 and
            is_bullish_candle3 and
            closes_above_candle1_close)

def is_separating_lines(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    candle1 = df.iloc[index - 1]
    candle2 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False  # Return False if the second candle has no range

    # Check if Candle 1 is bullish and Candle 2 is bearish
    is_bullish_candle1 = o1 < c1
    is_bearish_candle2 = o2 > c2
    
    # Check if Candle 2 opens above the close of Candle 1 and closes below the open of Candle 1
    opens_above_candle1_close = o2 > c1
    closes_below_candle1_open = c2 < o1
    
    # Check if Candle 2's body covers Candle 1's body
    covers_candle1_body = (o2 < o1 and c2 > c1)
    
    return (is_bullish_candle1 and
            is_bearish_candle2 and
            opens_above_candle1_close and
            closes_below_candle1_open and
            covers_candle1_body)

def is_shooting_star(open_price, close_price, high_price, low_price, body_threshold=0.1, shadow_ratio=2):
    body_length = abs(open_price - close_price)
    if high_price == low_price:
        return False 
    candle_range = high_price - low_price
    upper_shadow_length = high_price - max(open_price, close_price)
    lower_shadow_length = min(open_price, close_price) - low_price
    
    # Check if the body is small relative to the total range
    is_small_body = body_length / candle_range < body_threshold
    # Check if the upper shadow is at least twice as long as the body
    is_long_upper_shadow = upper_shadow_length >= body_length * shadow_ratio
    # Check if the lower shadow is minimal
    is_small_lower_shadow = lower_shadow_length <= body_length * 0.1
    
    return is_small_body and is_long_upper_shadow and is_small_lower_shadow


def is_short_line(open_price, close_price, high_price, low_price, body_threshold=0.1):
    body_length = abs(open_price - close_price)
    if high_price == low_price:
        return False 
    candle_range = high_price - low_price
    
    # Check if the body is small relative to the total range
    is_small_body = body_length / candle_range < body_threshold
    
    return is_small_body


def is_spinning_top(open_price, close_price, high_price, low_price, body_threshold=0.1, shadow_ratio=2):
    body_length = abs(open_price - close_price)
    if high_price == low_price:
        return False 
    candle_range = high_price - low_price
    upper_shadow_length = high_price - max(open_price, close_price)
    lower_shadow_length = min(open_price, close_price) - low_price
    
    # Check if the body is small relative to the total range
    is_small_body = body_length / candle_range < body_threshold
    # Check if both shadows are relatively long compared to the body
    is_long_upper_shadow = upper_shadow_length >= body_length * shadow_ratio
    is_long_lower_shadow = lower_shadow_length >= body_length * shadow_ratio
    
    return is_small_body and is_long_upper_shadow and is_long_lower_shadow


def is_stalled_pattern(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False  # Return False if the second candle has no range

    # Check if the pattern matches Stalled Pattern criteria
    is_bullish_candle1 = o1 < c1
    is_small_body_candle2 = abs(o2 - c2) < (h2 - l2) * 0.3
    is_bearish_candle3 = o3 > c3
    is_candle3_closes_below_midpoint_candle1 = c3 < (o1 + c1) / 2

    return (is_bullish_candle1 and
            is_small_body_candle2 and
            is_bearish_candle3 and
            is_candle3_closes_below_midpoint_candle1)


def is_stick_sandwich(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False  # Return False if the second candle has no range

    # Check if the pattern matches Stick Sandwich criteria
    is_bullish_candle1 = o1 < c1
    is_small_body_candle2 = abs(o2 - c2) < (h2 - l2) * 0.3
    is_bearish_candle3 = o3 > c3
    is_candle2_within_candle1 = (l1 < l2 < h1) and (l1 < h2 < h1)
    is_candle3_closes_below_candle1_open = c3 < o1
    
    return (is_bullish_candle1 and
            is_small_body_candle2 and
            is_bearish_candle3 and
            is_candle2_within_candle1 and
            is_candle3_closes_below_candle1_open)

def is_takuri(open_price, close_price, high_price, low_price, body_threshold=0.1, shadow_ratio=2):
    body_length = abs(open_price - close_price)
    if high_price == low_price:
        return False 
    candle_range = high_price - low_price
    lower_shadow_length = min(open_price, close_price) - low_price
    upper_shadow_length = high_price - max(open_price, close_price)
    
    # Check if the body is small relative to the total range
    is_small_body = body_length / candle_range < body_threshold
    # Check if the lower shadow is at least twice as long as the body
    is_long_lower_shadow = lower_shadow_length >= body_length * shadow_ratio
    # Check if the upper shadow is minimal
    is_small_upper_shadow = upper_shadow_length <= body_length * 0.1
    
    return is_small_body and is_long_lower_shadow and is_small_upper_shadow

def is_tasukigap(df, index, gap_threshold=1):
    if index < 1:
        return False
    
    # Get the two most recent candles
    prev_candle = df.iloc[index - 1]
    current_candle = df.iloc[index]
    
    # Extract open, close, high, and low prices
    prev_close = float(prev_candle['ltp'])
    curr_open = float(current_candle['open'].replace(',',''))
    
    # Check if there is a significant gap
    gap_size = abs(curr_open - prev_close)
    
    return gap_size >= gap_threshold

def is_thrusting(df, index):
    if index < 1:
        return False
    
    # Get the two most recent candles
    prev_candle = df.iloc[index - 1]
    curr_candle = df.iloc[index]
    
    # Extract open, close, high, and low prices
    prev_open, prev_close, prev_high, prev_low = float(prev_candle['open'].replace(',','')), float(prev_candle['ltp']), float(prev_candle['high']), float(prev_candle['low'])
    curr_open, curr_close, curr_high, curr_low = float(curr_candle['open'].replace(',','')), float(curr_candle['ltp']), float(curr_candle['high']), float(curr_candle['low'])
    
    # Check if the previous candle is bullish (uptrend) or bearish (downtrend)
    is_prev_bullish = prev_open < prev_close
    is_prev_bearish = prev_open > prev_close
    
    # Check if the current candle's body is within the range of the previous candle's body but does not completely engulf it
    is_thrusting_candle = (curr_open < prev_close and curr_close > prev_open and
                           (curr_open < prev_close and curr_close > prev_open))
    
    # For bearish Thrusting: previous candle should be bullish and current candle should have a body that extends into the previous candle's body but does not completely engulf it
    if is_prev_bullish:
        return (curr_open < prev_close and curr_close > prev_open and curr_close < prev_open and curr_open < prev_close)
    
    # For bullish Thrusting: previous candle should be bearish and current candle should have a body that extends into the previous candle's body but does not completely engulf it
    if is_prev_bearish:
        return (curr_open > prev_close and curr_close < prev_open and curr_close > prev_open and curr_open > prev_close)
    
    return False


def is_tri_star(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    prev_candle = df.iloc[index - 2]
    middle_candle = df.iloc[index - 1]
    curr_candle = df.iloc[index]
    
    # Extract open, close, high, and low prices
    p_open, p_close, p_high, p_low = float(prev_candle['open'].replace(',','')), float(prev_candle['ltp']), float(prev_candle['high']), float(prev_candle['low'])
    m_open, m_close, m_high, m_low = float(middle_candle['open'].replace(',','')), float(middle_candle['ltp']), float(middle_candle['high']), float(middle_candle['low'])
    c_open, c_close, c_high, c_low = float(curr_candle['open'].replace(',','')), float(curr_candle['ltp']), float(curr_candle['high']), float(curr_candle['low'])
    candle2_range = m_high - m_low
    if candle2_range == 0:
        return False  # Return False if the second candle has no range

    # Determine if the pattern is a bearish or bullish TriStar
    is_prev_bullish = p_open < p_close
    is_prev_bearish = p_open > p_close
    is_middle_doji = abs(m_open - m_close) / (m_high - m_low) < 0.1
    is_curr_bullish = c_open < c_close
    is_curr_bearish = c_open > c_close
    
    # Conditions for a bearish TriStar
    if is_prev_bullish:
        return (is_middle_doji and
                (m_low < p_low and m_high > p_high) and
                is_curr_bearish and
                c_open < m_low and c_close < p_low and c_close < m_open)
    
    # Conditions for a bullish TriStar
    if is_prev_bearish:
        return (is_middle_doji and
                (m_low < p_low and m_high > p_high) and
                is_curr_bullish and
                c_open > m_high and c_close > p_high and c_close > m_open)
    
    return False

def is_unique_3_river(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    prev_candle = df.iloc[index - 2]
    middle_candle = df.iloc[index - 1]
    curr_candle = df.iloc[index]
    
    # Extract open, close, high, and low prices
    p_open, p_close, p_high, p_low = float(prev_candle['open'].replace(',','')), float(prev_candle['ltp']), float(prev_candle['high']), float(prev_candle['low'])
    m_open, m_close, m_high, m_low = float(middle_candle['open'].replace(',','')), float(middle_candle['ltp']), float(middle_candle['high']), float(middle_candle['low'])
    c_open, c_close, c_high, c_low = float(curr_candle['open'].replace(',','')), float(curr_candle['ltp']), float(curr_candle['high']), float(curr_candle['low'])
    candle2_range = m_high - m_low
    if candle2_range == 0:
        return False  # Return False if the second candle has no range

    # Determine if the pattern is Unique 3 River
    is_first_bullish = p_open < p_close
    is_middle_doji = abs(m_open - m_close) / (m_high - m_low) < 0.1
    is_curr_bearish = c_open > c_close
    is_curr_gaps_down = c_open < m_low
    is_curr_closes_below_prev_close = c_close < p_close
    
    return (is_first_bullish and
            is_middle_doji and
            is_curr_bearish and
            is_curr_gaps_down and
            is_curr_closes_below_prev_close)

def is_upside_gap_two_crows(df, index):
    if index < 2:
        return False
    
    # Get the three most recent candles
    candle1 = df.iloc[index - 2]
    candle2 = df.iloc[index - 1]
    candle3 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False  # Return False if the second candle has no range

    # Determine if the pattern is Upside Gap Two Crows
    is_first_bullish = o1 < c1
    is_second_small_body = abs(o2 - c2) < (h2 - l2) * 0.3
    is_second_open_above_first_close = o2 > c1
    is_second_close_within_first_body = l1 < c2 < h1
    is_third_bearish = o3 > c3
    is_third_open_within_second_body = o2 < o3 < c2
    is_third_closes_below_first_low = c3 < l1

    return (is_first_bullish and
            is_second_small_body and
            is_second_open_above_first_close and
            is_second_close_within_first_body and
            is_third_bearish and
            is_third_open_within_second_body and
            is_third_closes_below_first_low)

def is_x_side_gap_three_methods(df, index):
    if index < 3:
        return False
    
    # Get the four most recent candles
    candle1 = df.iloc[index - 3]
    candle2 = df.iloc[index - 2]
    candle3 = df.iloc[index - 1]
    candle4 = df.iloc[index]
    
    # Extract open, close, high, and low prices
    o1, c1, h1, l1 = float(candle1['open'].replace(',','')), float(candle1['ltp']), float(candle1['high']), float(candle1['low'])
    o2, c2, h2, l2 = float(candle2['open'].replace(',','')), float(candle2['ltp']), float(candle2['high']), float(candle2['low'])
    o3, c3, h3, l3 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    o4, c4, h4, l4 = float(candle3['open'].replace(',','')), float(candle3['ltp']), float(candle3['high']), float(candle3['low'])
    candle2_range = h2 - l2
    if candle2_range == 0:
        return False  # Return False if the second candle has no range

    # Determine if the pattern is X-Side Gap Three Methods
    is_first_bullish = o1 < c1
    is_second_small_body = abs(o2 - c2) < (h2 - l2) * 0.3
    is_third_small_body = abs(o3 - c3) < (h3 - l3) * 0.3
    is_second_gap_above_first_close = o2 > c1
    is_third_gap_above_second_close = o3 > c2
    is_fourth_bullish = o4 < c4
    is_fourth_close_above_first_high = c4 > h1

    return (is_first_bullish and
            is_second_small_body and
            is_third_small_body and
            is_second_gap_above_first_close and
            is_third_gap_above_second_close and
            is_fourth_bullish and
            is_fourth_close_above_first_high)



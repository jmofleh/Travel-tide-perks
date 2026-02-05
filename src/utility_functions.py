
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# -----------------------------
# DATA CLEANING
# -----------------------------

def remove_infinite_and_nan(df):
    """Replace inf/-inf with NaN and fill NaN with 0."""
    return df.replace([np.inf, -np.inf], np.nan).fillna(0)


def calculate_session_duration(df):
    """Create session_duration in seconds from start and end timestamps."""
    df['session_start'] = pd.to_datetime(df['session_start'])
    df['session_end'] = pd.to_datetime(df['session_end'])
    df['session_duration'] = (df['session_end'] - df['session_start']).dt.total_seconds()
    return df


# -----------------------------
# OUTLIERS
# -----------------------------

def iqr_bounds(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


def remove_outliers_iqr(df, column):
    lower, upper = iqr_bounds(df[column])
    return df[(df[column] >= lower) & (df[column] <= upper)]


# -----------------------------
# FEATURE ENGINEERING
# -----------------------------

def hotel_hunter_index(num_hotels, num_trips):
    return num_hotels / (num_trips + 1)


def flight_fanatic_index(num_flights, num_trips):
    return num_flights / (num_trips + 1)


def bundle_index(num_bundle_trips, num_trips):
    return num_bundle_trips / (num_trips + 1)


def calculate_discount_percentage(amount, base_price):
    return np.where(base_price > 0, (amount / base_price) * 100, 0)


# -----------------------------
# HAVERSINE DISTANCE
# -----------------------------

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    c = 2*np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c


# -----------------------------
# SCALING
# -----------------------------

def scale_features(df):
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df)
    return pd.DataFrame(scaled, columns=df.columns, index=df.index)


# -----------------------------
# SPEND CALCULATIONS
# -----------------------------

def compute_flight_spend(seats, base_fare):
    return seats.fillna(0) * base_fare.fillna(0)


def compute_hotel_spend(nights, rooms, price):
    nights = nights.clip(lower=0)
    return nights.fillna(0) * rooms.fillna(0) * price.fillna(0)


# -----------------------------
# SUMMARY HELPERS
# -----------------------------

def count_nulls(df):
    return df.isnull().sum()


def print_shape(df, name="DataFrame"):
    print(f"{name} shape: {df.shape}")

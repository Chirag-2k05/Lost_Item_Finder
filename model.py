import datetime

import numpy as np

from db import get_items


def predict_location(user, item):
    data = get_items(user, item)

    if not data:
        return None, 0

    current_time = datetime.datetime.now()

    best_score = -1
    best_location = None

    for row in data:
        timestamp = datetime.datetime.fromisoformat(row[3])
        confidence = row[4]
        location = row[2]

        time_diff = (current_time - timestamp).total_seconds()

        score = 0.6 * confidence + 0.4 * np.exp(-time_diff / 200000)

        if score > best_score:
            best_score = score
            best_location = location

    return best_location, round(best_score, 3)
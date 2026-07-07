from app.db.mongo import event_details_collection


def weather_condition_summary():
    """
    Aggregation pipeline: groups events by weather condition,
    calculating average temperature and listing event titles per condition.
    """
    pipeline = [
        {
            "$match": {"weather_summary.conditions": {"$ne": None}}
        },
        {
            "$group": {
                "_id": "$weather_summary.conditions",
                "event_count": {"$sum": 1},
                "average_temperature": {"$avg": "$weather_summary.temperature"},
                "sample_events": {"$push": "$description"}
            }
        },
        {
            "$sort": {"event_count": -1}
        }
    ]

    results = list(event_details_collection.aggregate(pipeline))
    return results


def tag_frequency_summary():
    """
    Aggregation pipeline: unwinds the tags array and counts
    frequency of each tag across all events.
    """
    pipeline = [
        {"$unwind": "$tags"},
        {
            "$group": {
                "_id": "$tags",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}}
    ]

    results = list(event_details_collection.aggregate(pipeline))
    return results


if __name__ == "__main__":
    print("=== Weather Condition Summary ===")
    for row in weather_condition_summary():
        print(f"{row['_id']}: {row['event_count']} events, avg temp {row['average_temperature']:.1f}°C")

    print("\n=== Tag Frequency Summary ===")
    for row in tag_frequency_summary():
        print(f"{row['_id']}: {row['count']} occurrences")

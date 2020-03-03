def get_stops_by_route_type(feed, route_type):
    """
    Filters a GTFS feed for a specific route type and returns stops that match that route type.
    """
    route_ids = feed.routes[feed.routes["route_type"] == route_type]["route_id"]
    trip_ids = feed.trips[feed.trips["route_id"].isin(route_ids)]["trip_id"]
    stop_ids = feed.stop_times[feed.stop_times["trip_id"].isin(trip_ids)]["stop_id"]
    return feed.stops[feed.stops["stop_id"].isin(set(stop_ids))]

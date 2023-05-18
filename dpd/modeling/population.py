from pandas import DataFrame


class Population(DataFrame):
    @staticmethod
    def from_trip_dataframe(trip_dataframe):
        population = []
        for origin in trip_dataframe.index:
            for destination in trip_dataframe.columns:
                for number_of_trips in range(trip_dataframe[destination][origin]):
                    population.append({"origin": origin, "destination": destination})
        return Population(people)

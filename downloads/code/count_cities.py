from geological_data import US_STATES 
from magic_geocoding_library import geocode_address

def build_query_locations(city):
    return ['%s, %s, USA' % (city, state) for state in US_STATES]

def find_matching_states(places_to_geocode, city_to_match):
    """Create a list of each state we found a geocoder result matching our city."""
    geocoding_results = [geocode_address(place) for place in places_to_geocode]

    matching_states = []
    for result in geocoding_results:
        _geocode_had_matching_state = (
            result is not None and
            result.city == city_to_match)
        if _geocode_had_matching_state:
            matching_states.append(result.state)
    return matching_states

def main():
    """Find out what states contain cities of a given name."""
    city_to_match = raw_input('Please enter a city: ')
    places_to_geocode = build_query_locations(city_to_match)
    matching_states = find_matching_states(places_to_geocode, city_to_match)

    print 'Matches for %s:' % city_to_match
    for state in matching_states:
        print 'Found match in %s!' % state

if __name__ == '__main__':
    main()

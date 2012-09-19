from count_cities import geocode_address
from count_cities import find_matching_states
from mock import Mock
from mock import patch
from unittest import TestCase

class CountCitiesTestCase(TestCase):
    def test_handle_none_geocoder_responses(self):
        """Make sure find_matching_businesses doesn't break if our geocoder
        result is None.
        
        Also test we are calling geocode_address once per place and that we get
        no matches in return.
        """

        city_to_match = 'Buttonwillow'
        place_to_geocode = ['%s, CA' % city_to_match]
        # Inside this context manager, we've mocked out the geocode_address
        # method to return None whenever it is called.
        with patch.object('geocode_address', new=Mock(return_value=None)):
            matching_states = find_matching_states(place_to_geocode, city_to_match)

        # Check that we called geocode_address once per place
        assert len(geocode_address.call_list) == len(places_to_geocode)
        # Assert we always called with what we expected
        for place, call_args in zip(places_to_geocode, geocode_address.call_list):
            assert call_args == (place, city_to_match)
        # And just for completeness, assert that we returned no matches
        assert matching_states == []

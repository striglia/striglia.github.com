from collections import namedtuple

CUSTOMER_FIELDS = ['name', 'has_vip_membership']
class Customer(namedtuple('_Customer', CUSTOMER_FIELDS)):
    """
    A mini-class used to represent a person trying to get a table at an 
    exclusive restaurant. The data is all immutable and the
    deserves_vip_seating property handles the hard thinking.
    """
    @property
    def deserves_chefs_table(self):
        """Returns True if this customer should be seated at the chef's table."""
        return self.has_vip_membership or self.name == 'Barack Obama'

if __name__ == '__main__':
    customer_info = [
        {'name': 'Roger Moore', 'has_vip_membership': False},
        {'name': 'Sean Connery', 'has_vip_membership': True},
        {'name': 'Barack Obama', 'has_vip_membership': False}]

    customers = [Customer(**c) for c in customer_info]
    for c in customers:
        if c.deserves_chefs_table:
            print "Send %s to the chef's table!" % c.name

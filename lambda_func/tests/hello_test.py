import unittest
from lambda_func import hello


class TestHello(unittest.TestCase):
    """
    This tests our Hello intent.
    The intent itself is very simple and short, thus our tests are also
    """

    @classmethod
    def setUpClass(cls):
        """ Setup the intent for the tests. """

        # Set the 'random' responses to only one response for easier 'randomness' checking
        hello._randoms = ['Testing']

        # The amount of tests we run
        cls.test_amount = 100000

    @staticmethod
    def extract_resp(resp):
        """
        Helper function for extracting the content of the reponse.
        """
        return resp.get('dialogAction', {}).get('message', {}).get('content', None)

    def test_hello(self):
        """
        The test itself, we run as many iterations as defined by _test_amount_.
        We also calculate the amount of times a 'random' reponse occurs.
        """

        # Counting the amount of 'random' responses
        count = 0
        for i in range(0, self.test_amount):
            # Run the intent
            res = hello.hello_handler()
            # Extract the response
            res = self.extract_resp(res)
            # Check that a proper response (i.e. string) was returned
            self.assertTrue(
                type(res) == str and res != '',
                'Did not get a hello response message, instead: {}'.format(res))
            # And if the result was our defined test 'random' string, increment the counter
            if res == 'Testing':
                count += 1
        
        # Here we now calculate the percentage amount of times the 'random' response got out
        calc = count / self.test_amount
        # Check that the percentage amount does not exceed the amount (+1) set by the intent itself
        self.assertTrue(
            calc <= hello._perc_chance + 1,
            'Random responses were too frequent {} %'.format(calc))


import sys
sys.path.append("../../../")

from authority.authorizer import Authorizer
import falcon

class Preprocess(object):
    def process_request(self, req, resp):
        token = req.get_header('token')

        challenges = ['token="bxixwiw"']
        if token is None:
            description = ('Please provide an auth token '
                           'as part of the request.')

            raise falcon.HTTPUnauthorized('Auth token required',
                                          description,
                                          challenges,
                                          href='http://docs.example.com/auth')
        if not Authorizer().verify_token(token):
            description = ('The provided auth token is not valid. '
                           'Please request a new token and try again.')
            raise falcon.HTTPUnauthorized('Authentication required',
                                          description,
                                          challenges,
                                          href='http://docs.example.com/auth')




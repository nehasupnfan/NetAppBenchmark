import sys, os, requests

sys.path.append('../')
sys.path.append('../../')

from authority.authorizer import Authorizer


class MasterComm:
    def __init__(self):
        pass

    def send_to_master(self, **kwargs):
        headers = {'token': kwargs["token"]}
        try:
            response = requests.post(kwargs["api"], data=kwargs["payload"], headers=headers)
        except Exception as e:
            raise e
        #print(response)



    def communicate_message(self, **kwargs):
        encoded_jwt = Authorizer().create_token()
        if "value" in kwargs.keys():
           payload = '{"%s" : "%s", "value": "%s"}' % (kwargs["route"], kwargs["msg"], kwargs["value"])
        else:
            payload = '{"%s" : "%s"}' % (kwargs["route"], kwargs["msg"])
        self.send_to_master(api=kwargs["url"] + "/" + kwargs["route"], token=encoded_jwt, payload=payload)







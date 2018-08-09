
class ServiceError(Exception):
    def __init__(self, name=None, code=None, message=None, data=None, error=None):
        super(ServiceError, self).__init__(message)
        self.name = name
        self.code = code
        self.message = '' if message is None else message
        self.data = data or error or ''
        # data = JSON RPC 2.0, error = 1.1

    # def __str__(self):
    #     return self.name + ': ' + str(self.code) + '. ' + self.message + \
    #         '\n' + self.data
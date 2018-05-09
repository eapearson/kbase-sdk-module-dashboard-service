from DashboardService.GenericClient import GenericClient


class UserProfileCache(object):
    def __init__(self, url=None):
        if url is None:
            raise ValueError('the "url" argument is required')
        self.url = url

        self.profiles = dict()

        self.rpc = GenericClient(
            module='UserProfile',
            url=self.url,
            token=None
        )

    def load(self):
        result, error = self.rpc.call_func('filter_users', [{
            'filter': ''
        }])
        if error:
            raise ValueError(error)

        users = result[0]

        # Annoying, but we need to turn around and get the full profiles now.

        usernames = [user['username'] for user in users]
        result, error = self.rpc.call_func('get_user_profile', [
            usernames
        ])
        if error:
            raise ValueError(error)

        profiles = result[0]

        for profile in profiles:
            self.profiles[profile['user']['username']] = profile

    def find(self, usernames=None):
        profiles = []
        for username in usernames:
            if username in self.profiles:
                profiles.append(self.profiles[username])
            else:
                profiles.append(None)
        return profiles


from DashboardService.GenericClient import GenericClient


class AppCache(object):
    def __init__(self, nms_url=None):
        if nms_url is None:
            raise ValueError('the "nms_url" argument is required')
        self.nms_url = nms_url

        self.nms_apps = {
            'release': dict(),
            'beta': dict(),
            'dev': dict()
        }

        self.rpc = GenericClient(
            module='NarrativeMethodStore',
            url=self.nms_url,
            token=None
        )

    def load_for_tag(self, tag):
        result, error = self.rpc.call_func('list_methods', [{
            'tag': tag
        }])
        if error:
            raise ValueError(error)
        for app in result[0]:
            self.nms_apps[tag][app['id']] = {
                'info': app,
                'tag': tag
            }

    def load(self):
        self.load_for_tag('release')
        self.load_for_tag('beta')
        self.load_for_tag('dev')

    def find(self, app_ref):
        if app_ref in self.nms_apps['release']:
            return self.nms_apps['release'][app_ref]
        elif app_ref in self.nms_apps['beta']:
            return self.nms_apps['beta'][app_ref]
        elif app_ref in self.nms_apps['dev']:
            return self.nms_apps['dev'][app_ref] 
        else:
            return None

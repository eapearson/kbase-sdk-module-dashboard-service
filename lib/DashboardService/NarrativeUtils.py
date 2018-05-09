class WorkspaceIdentity(object):
    def __init__(self, workspace=None, id=None):
        if (workspace is None):
            if (id is None):
                raise ValueError('either "workspace" or "id" are required')   
        elif (id is not None):
            raise ValueError('only one of "workspace" or "id" may be provided')
        self.workspace_name = workspace
        self.workspace_id = id

    def make_wsi(self):
        return {
            'workspace': self.workspace_name,
            'id': self.workspace_id
        }

    def workspace(self):
        return self.workspace_name

    def id(self):
        return self.workspace_id


class NarrativeUtils(object):
    def __init__(self, workspace_client=None):
        if (workspace_client is None):
            raise ValueError('"workspace_client" argument is required')

        self.workspace_client = workspace_client

    def delete_narrative(self, wsi=None):
        if (wsi is None):
            raise ValueError('"wsi" is required')

        self.workspace_client.delete_workspace(wsi.make_wsi())
        pass

    def share_narrative(self, wsi=None, users=None, permission=None):
        if (wsi is None):
            raise ValueError('"wsi" is required')
        if (users is None):
            raise ValueError('"users" is required')
        if (permission is None):
            raise ValueError('"permission" is required')                        

        self.workspace_client.set_permissions({
            'workspace': wsi.workspace(),
            'id': wsi.id(),
            'new_permission': permission,
            'users': users
        })
        pass

    def unshare_narrative(self, wsi=None, users=None):
        if (wsi is None):
            raise ValueError('"wsi" is required')
        if (users is None):
            raise ValueError('"users" is required')

        self.workspace_client.set_permissions({
            'workspace': wsi.workspace(),
            'id': wsi.id(),
            'new_permission': 'n',
            'users': users
        })
        pass

    def share_narrative_global(self, wsi=None):
        if (wsi is None):
            raise ValueError('"wsi" is required')

        self.workspace_client.set_global_permission({
            'workspace': wsi.workspace(),
            'id': wsi.id(),
            'new_permission': 'r',
        })
        pass

    def unshare_narrative_global(self, wsi=None):
        if (wsi is None):
            raise ValueError('"wsi" is required')

        self.workspace_client.set_global_permission({
            'workspace': wsi.workspace(),
            'id': wsi.id(),
            'new_permission': 'n',
        })
        pass

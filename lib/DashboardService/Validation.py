import math
import json
import time
import calendar
import re

class Validation(object):

    @staticmethod
    def check_param(params, name, required, param_type):
        if name not in params:
            if required:
                error = {
                    'message': 'the required parameter "' + name + '" was not provided',
                    'type': 'input',
                    'code': 'missing',
                    'info': {
                        'key': name
                    }
                }
                return None, error
            else:
                return None, None

        param_value = params[name]
        if not isinstance(param_value, param_type):
            error = {
                'message': ('the "' + name + '" parameter is expected to be a "' + param_type.__name__ + '" but is actually a "' + type(param_value).__name__),
                'type': 'input',
                'code': 'wrong-type',
                'info': {
                    'key': name,
                    'expected': param_type.__name__,
                    # TODO translate to json type name
                    'received': type(param_value).__name__
                }
            }
            return None, error
        return param_value, None

    @classmethod
    def validate_list_all_narratives(cls, ctx, parameter):
        # nothing to do yet...
        just_modified_after, error = cls.check_param(parameter, 'just_modified_after', False, basestring)
        if error:
            return None, error

        return {
            'just_modified_after': just_modified_after
        }, None

    @classmethod
    def validate_create_narrative(cls, ctx, parameter):
        # nothing to do yet...
        title, error = cls.check_param(parameter, 'title', True, basestring)
        if error:
            return None, error

        name, error = cls.check_param(parameter, 'name', False, basestring)
        if error:
            return None, error

        return {
            'title': title,
            'name': name
        }, None

    @classmethod
    def validate_delete_narrative(cls, ctx, parameter):
        obji, error = cls.check_param(parameter, 'obji', True, dict)
        if error:
            return None, error

        return {
            'obji': obji
        }, None

    @classmethod
    def validate_share_narrative(cls, ctx, parameter):
        wsi, error = cls.check_param(parameter, 'wsi', True, dict)
        if error is not None:
            return None, error

        users, error = cls.check_param(parameter, 'users', True, list)
        if error is not None:
            return None, error

        permission, error = cls.check_param(parameter, 'permission', True, basestring)
        if error is not None:
            return None, error

        return {
            'wsi': wsi,
            'users': users,
            'permission': permission
        }, None

    @classmethod
    def validate_unshare_narrative(cls, ctx, parameter):
        wsi, error = cls.check_param(parameter, 'wsi', True, dict)
        if error is not None:
            return None, error

        users, error = cls.check_param(parameter, 'users', True, list)
        if error is not None:
            return None, error

        return {
            'wsi': wsi,
            'users': users
        }, None

    @classmethod
    def validate_share_narrative_global(cls, ctx, parameter):
        wsi, error = cls.check_param(parameter, 'wsi', True, dict)
        if error is not None:
            return None, error

        return {
            'wsi': wsi
        }, None

    @classmethod
    def validate_unshare_narrative_global(cls, ctx, parameter):
        wsi, error = cls.check_param(parameter, 'wsi', True, dict)
        if error is not None:
            return None, error

        return {
            'wsi': wsi
        }, None

    @classmethod
    def validate_config(cls, config):
        for name in ['cache-directory', 'workspace-url', 'service-wizard', 
                     'narrative-method-store-url', 'user-profile-service-url']:
            value, error = cls.check_param(config, name, True, basestring)
            if error:
                return None, error['message']

        return {
            'services': {
                'Workspace': config['workspace-url'],
                'NarrativeMethodStore': config['narrative-method-store-url'],
                'UserProfile': config['user-profile-service-url'],
                'ServiceWizard': config['service-wizard']
            },
            'caches': {
                'object': {
                    'path': config['cache-directory'] + '/object_cache.db'
                },
                'userprofile': {
                    'path': config['cache-directory'] + '/user_profile_cache.db'
                },
                'app': {
                    'path': config['cache-directory'] + '/app_cache.db'
                },
                'workspace': {
                    'path': config['cache-directory'] + '/workspace_cache.db'
                },
                'narrative': {
                    'path': config['cache-directory'] + '/narrative_cache.db'
                }
            }
        }, None
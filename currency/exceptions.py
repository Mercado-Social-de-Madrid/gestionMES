# coding=utf-8
import json

from tastypie.http import HttpForbidden


class AllInvitesSent(Exception):
    """ Exception when a transaction is being made but the wallet doesnt have enough cash """
    def __init__(self, invitations_used=None):

        response = {
            'error': 'all_invites_sent',
            'message': 'Ya has enviado el máximo de invitaciones disponibles'
        }
        if invitations_used:
            response['invitations_used'] = invitations_used

        self.response = HttpForbidden(content=json.dumps(response), content_type='application/json')


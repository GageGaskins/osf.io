#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
from modularodm import Q

from website.app import init_app
from scripts import utils as script_utils
from framework.transactions.context import TokuTransaction

from website.addons.dataverse.model import AddonDataverseNodeSettings

logger = logging.getLogger(__name__)


def do_migration(records, dry=True):
    with TokuTransaction():
        for node_addon in AddonDataverseNodeSettings.find(Q('foreign_user_settings', 'ne', None)):
            user_addon = node_addon.foreign_user_settings
            if not user_addon.external_accounts:
                logger.warning('User {0} has not dataverse external account'.format(user_addon.owner._id))
            account = user_addon.external_account[0]
            if not dry:
                node_addon.set_auth(account, user_addon.owner)
            logger.info('Added external account {0} to node {1}'.format(
                account._id, node_addon.owner._id,
            ))


def main(dry=True):
    init_app(set_backends=True, routes=False, mfr=False)  # Sets the storage backends on all models
    do_migration(dry=dry)


if __name__ == '__main__':
    dry = 'dry' in sys.argv
    if not dry:
        script_utils.add_file_logger(logger, __file__)
    main(dry=dry)

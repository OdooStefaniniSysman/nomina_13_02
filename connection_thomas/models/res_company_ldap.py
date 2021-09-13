# -*- coding: utf-8 -*-

from odoo import _, models, fields, api, tools
from odoo.tools.pycompat import to_text
from ldap.filter import filter_format
import os
import subprocess
import platform
import ldap
import sys
import logging
import paramiko


_logger = logging.getLogger(__name__)

class CompanyLDAP(models.Model):
    _inherit = 'res.company.ldap'

    def _authenticate(self, conf, login, password):
        if not password:
            return False

        host = '54.39.127.106'
        port, user, passwd = 1422, 'root', 'Soporte1'
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(host, port, user, passwd, timeout=10)
        command = "/usr/bin/python3 /root/ldap_connect.py " + "{} {}".format(login, "'" + password + "'") + " >> /dev/null"
        stdin, stdout, stderr = client.exec_command(command)
        errors = stderr.read()
        output = stdout.read()
        client.close()
        if login.upper() == errors.decode('UTF-8').rstrip().upper():
            return True
        return False

    def _map_ldap_attributes(self, conf, login, ldap_entry):
        host = '54.39.127.106'
        port, user, passwd = 1422, 'root', 'Soporte1'
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(host, port, user, passwd, timeout=10)
        command = "/usr/bin/python3 /root/ldap_connect_name.py " + login
        stdin, stdout, stderr = client.exec_command(command)
        errors = stderr.read()
        output = stdout.read()
        client.close()
        return {
            'name': output.decode('UTF-8').rstrip(),
            'login': login,
            'company_id': conf['company'][0]
        }

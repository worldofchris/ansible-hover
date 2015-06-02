#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: hover
short_description: Manage Hover.com DNS records
description:
    - Manages Hover.com DNS records via the unofficial/unsupported REST API.
      Records can be specified as being either present or absent.
author: Chris Young - worldofchris
notes:
    - Uses the hover-client module based on Dan Krause's gist U(https://gist.github.com/dankrause/5585907)
requirements:
 - "python >= 2.7"
 - hover-cleint U(https://github.com/worldofchris/hover-client)
 - "boto"
options:
    domain:
        description:
            - Domain for which to manage DNS records
        required: true
        default: null
        version_added: null
    username:
        description:
            - Hover.com username
        required: true
        default: null
        version_added: null
    password:
        description:
            - Hover.com password
        required: true
        default: null
        version_added: null
    state:
        description:
            - Should the record be present or absent?
        required: false
        default: present
        choices: [present, absent]
        version_added: null
    name:
        description:
            - DNS Record name
        required: true
        default: null
        version_added: null
    value:
        description:
            - Value of the DNS Record
        required: false
        default: null
        version_added: null
    type:
        description:
            - Record Type
        required: false
        default: A
        choices: ['A',
                  'ALIAS',
                  'CNAME',
                  'MX',
                  'SPF',
                  'URL',
                  'TXT',
                  'NS',
                  'SRV',
                  'NAPTR',
                  'PTR',
                  'AAAA',
                  'SSHFP',
                  'HINFO',
                  'POOL']
        version_added: null
'''

EXAMPLES = '''

# Ensure an CNAME record is present

- hover:
    username: bananas
    password: yell0w1s
    domain: worldofchris.com
    name: "staging"
    type: "CNAME"
    value: "ec2-51-12-65-192.eu-west-2.compute.amazonaws.com"
    state: present

# Ensure an A record is absent

- hover:
    username: bananas
    password: yell0w1s
    domain: worldofchris.com
    name: "demo"
    type: "A"
    state: absent

'''

RETURN = '''

'''

try:
    from hover.client import HoverClient, HoverException
    HAS_LIB = True
except:
    HAS_LIB = False


def main():

    module = AnsibleModule(
        argument_spec=dict(
            domain=dict(required=True),
            username=dict(required=True),
            password=dict(required=True, no_log=True),
            name=dict(required=True),
            value=dict(required=False, default=None),
            state=dict(required=False, choices=['present', 'absent'], default='present'),
            type=dict(requiured=False, choices=['A',
                                                'ALIAS',
                                                'CNAME',
                                                'MX',
                                                'SPF',
                                                'URL',
                                                'TXT',
                                                'NS',
                                                'SRV',
                                                'NAPTR',
                                                'PTR',
                                                'AAAA',
                                                'SSHFP',
                                                'HINFO',
                                                'POOL'], default='A'),
        ),
        add_file_common_args=True,
        supports_check_mode=True
    )

    if not HAS_LIB:
        module.fail_json(msg="Requires hover module")

    params = module.params
    changed = False

    try:
        hc = HoverClient(username=params['username'],
                         password=params['password'],
                         domain_name=params['domain'])

        record = hc.get_record(name=params['name'], type=params['type'])

        if params['state'] == 'present':

            if record is None:
                if not module.check_mode:
                    hc.add_record(name=params['name'],
                                  type=params['type'],
                                  content=params['value'])
                changed = True
            else:

                if record['content'] != params['value']:
                    if not module.check_mode:
                        hc.update_record(name=params['name'],
                                         type=params['type'],
                                         content=params['value'])
                    changed = True
        else:
            if record is not None:
                if not module.check_mode:
                    hc.remove_record(name=params['name'],
                                     type=params['type'])
                changed = True
    except HoverException as e:
        module.fail_json(msg=str(e))

    module.exit_json(changed=changed)

# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()

from django.utils.translation import ugettext_lazy as _  # noqa

from horizon import exceptions
from openstack_dashboard import api


def get_interfaces_data(self):
    try:
        router_id = self.kwargs['router_id']
        router = api.neutron.router_get(self.request, router_id)
        # Filter off the port on the mgt network and router external gateway
        ports = [
            api.neutron.Port(p) for p in router.ports
            if p['device_owner'] not in (
                'network:router_management',
                'network:router_gateway'
            )
        ]
    except Exception:
        ports = []
        msg = _(
            'Port list can not be retrieved for router ID %s' %
            self.kwargs.get('router_id')
        )
        exceptions.handle(self.request, msg)
    for p in ports:
        p.set_id_as_name_if_empty()
    return ports

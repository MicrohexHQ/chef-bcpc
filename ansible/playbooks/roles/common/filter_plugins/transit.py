from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

def transit_interfaces(a, *args, **kw):
  interfaces = []
  ansible_facts = args[0]

  for transit in a:
    interface = find_interface(facts=ansible_facts,
                               macaddress=transit['mac'])
    transit['name'] = interface['device']
    interfaces.append(transit)

  return interfaces

def find_interface(facts, macaddress):

  interfaces = facts['interfaces']

  for interface in interfaces:
    if interface == 'lo':
      continue
    if facts[interface]['macaddress'] == macaddress:
      return facts[interface]

  raise ValueError("could not find interface with mac: " + macaddress)

def update_chef_node(a, *args, **kw):

    node_details = a
    hostvars = args[0]

    interfaces = hostvars['interfaces']
    node_details['normal']['service_ip'] = interfaces['service']['ip']

    return node_details
    
class FilterModule(object):

  filter_map = {
    'transit_interfaces': transit_interfaces,
    'update_chef_node': update_chef_node,
  }

  def filters(self):
    return self.filter_map

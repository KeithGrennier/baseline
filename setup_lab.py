# Cml
import subprocess # for ping
"""

TODO 9k made me type cisco [ent] cisco...
###
TODO 9k line vty instead of line vty 0 15
TODO 9k ip domain-name
TODO how to solve minor things like this ^^^
"""
class Topology:
    def __init__(self):
        self.items=[]
    def append(self,values):
        self.items.append(values)
        return f'Adding {values} to Topology'
    def get(self,value:str):
        """
        value=hostname: str
        return valid device
        """
        for device in self.items:
            if device.hostname == value:
                return device.hostname
        return f'Device with hostname {value} not found'
    def get_all(self):
        return self.items
        
class Device:
    def __init__(self,device_type,ip,subnet,hostname):
        self.device_type=device_type
        self.ip=ip
        self.hostname=hostname
        self.subnet=subnet
        if self.device_type=='cat8k':
            self.interface='G4'
        elif self.device_type=='nxos9k':
            self.interface='mgmt0'
        else:
            self.interface=None
    def to_dict(self):
        return {
            'hostname':self.hostname,
            'ip':self.ip,
            'device_type':self.device_type,
            'subnet':self.subnet,
            'interface':self.interface
            }
    def __repr__(self):
        return f'<Device: {self.hostname}>'

def ssh(hostname:str,ip:str,subnet:str='255.255.255.0',domain:str='cisco.local',interface=None)->str:
    
    config=f"""
hostname {hostname}
ip domain name {domain}
interface {interface}
ip address {ip} {subnet}
no shutdown
exit
line vty 0 15
login local
transport input ssh
"""
    return config
def ping(ip:str):
    p=subprocess.Popen(f'ping {ip}')
    p.wait()
    return f'Ping {p.poll()}'

def main():
    ip_netmask='192.168.0.'
    ip_start_range=50
    my_subnet='255.255.255.0'
    hostname_delimiter='-'
    device_dict={
        'nxos9k':2,
        'cat8k':2,
        'asav':0,
        'csr':0,
        'iosv':0,
        'cat9k':0, # 9k made me type cisco [ent] cisco...
    }
    my_top=Topology()
    counter=0
    for key,value in device_dict.items():
        if counter >255:
            raise ValueError('IP address space maxed out')
        if value:
            for val in range(1,value+1,1):
                my_ip=ip_start_range+counter
                counter+=1
                my_ip=f'{ip_netmask}{my_ip}'
                temp_dev=(Device(device_type=key,ip=my_ip,subnet=my_subnet,hostname=f'{key}{hostname_delimiter}{val}'))
                my_top.append(temp_dev)
                # members = [attr for attr in dir(temp_dev) if not callable(getattr(temp_dev,attr)) and not attr.startswith("__")]
                # print(members)

                # print(temp_dev.hostname)
                # print(temp_dev.ip)
                # print(temp_dev.interface)
        
    print(my_top.get_all())
    devices_as_dict = [device.to_dict() for device in my_top.get_all()]
    print(devices_as_dict)
    for network_equipment in devices_as_dict:
        my_hostname=network_equipment.get('hostname')
        my_ip=network_equipment.get('ip')
        my_subnet=network_equipment.get('subnet')
        # domain:str='cisco.local',
        my_interface=network_equipment.get('interface')
        network_ssh_conf=ssh(hostname=my_hostname,ip=my_ip,subnet=my_subnet,interface=my_interface)
        print(network_ssh_conf)
    for network_equipment in devices_as_dict:
        print(ping(network_equipment.get('ip')))


if __name__ == '__main__':
    main()
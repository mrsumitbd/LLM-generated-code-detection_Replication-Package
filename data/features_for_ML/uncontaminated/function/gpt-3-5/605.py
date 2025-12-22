import json

def dump_distro_mapping(path: str):
    distro_mapping = {
        "Ubuntu": "Debian",
        "Fedora": "Red Hat",
        "CentOS": "Red Hat",
        "Arch": "Independent"
    }
    
    with open(path, 'w') as file:
        json.dump(distro_mapping, file)
import json
import os

def dump_distro_mapping(path: str):
    distro_mapping = {
        "Ubuntu": "ubuntu",
        "Debian": "debian",
        "CentOS": "centos",
        "RHEL": "rhel",
        "Fedora": "fedora",
        "openSUSE": "opensuse",
        "Arch Linux": "arch",
        "Gentoo": "gentoo",
        "Manjaro": "manjaro",
        "Kali Linux": "kali"
    }

    with open(path, "w") as file:
        json.dump(distro_mapping, file, indent=4)
from typing import List

def site_config_dirs(appname: str) -> List[str]:
    return [f'/etc/{appname}', f'/usr/local/etc/{appname}']
def get_version_from_url(download_url):
    try:
        version = download_url.split('/')[-1].split('-')[-1].split('.')[0]
        return version
    except:
        return None
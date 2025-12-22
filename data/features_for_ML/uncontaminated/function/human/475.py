import os

def get_aksk():
    ak = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
    sk = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    sts = os.getenv('ALIBABA_CLOUD_SECURITY_TOKEN')
    header = current_request_headers.get()
    if header and (header.get("ak") or header.get("sk") or header.get("sts")):
        ak, sk, sts = header.get("ak"), header.get("sk"), header.get("sts")
    return ak, sk, sts
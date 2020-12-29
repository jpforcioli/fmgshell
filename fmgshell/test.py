# coding=utf-8

import fmgjsonrpcapi

fmg = fmgjsonrpcapi.FMGJSONRPCAPI()
fmg.login("secops-labs-004.gcp.fortipoc.net", "devops", "fortinet", port=10407)

url = "/um/object/list"
payload = {
    "data": {
        "used_only": 1,
        "version_list": 1,
    },
}

fmg.debug("on")
fmg.get(url, payload)
fmg.debug("off")

fmg.logout()
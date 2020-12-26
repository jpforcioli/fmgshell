# coding=utf-8

import fmgjsonrpcapi

fmg = fmgjsonrpcapi.FMGJSONRPCAPI()
fmg.login("secops-labs-004.gcp.fortipoc.net", "devops", "fortinet", port=10407)

attributes = {
    "option": ["syntax"],
}

fmg.debug("on")
fmg.get("/", attributes)
fmg.debug("off")

fmg.logout()
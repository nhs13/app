import json


def gen_msg(bool, msg, format="json"):
    action = "successful"
    if bool != True:
        action = f"un{action}"
    res = {"action": action, "msg": msg}
    if format == "json":
        return json.dumps(res)
    return res

import src.KeyValueList as mKvList
import json

def get_id_by_name(p_members: list, p_name: str, p_discriminator=None):
    members = p_members
    m_id = None
    for m in members:
        m_fullname = str(m).lower()
        m_name = str(m.name).lower()
        # print(f"{m_name}:{type(m_name)} == {p_name}:{type(p_name)} ? {m_name == p_name.lower()}")
        if m_name == p_name.lower():
            m_id = m.id

        if p_discriminator is not None:
            p_name = p_name + "#" + p_discriminator
            p_name.lower()
        if m_fullname == p_name.lower():
            m_id = m.id
    return m_id


def is_online(p_members: list, p_id_or_name):
    for m in p_members:
        status = str(m.status)
        if m.id == p_id_or_name:
            if status == "online":
                return True
        if m.name == p_id_or_name:
            if status == "online":
                return True
        if str(m) == p_id_or_name:
            if status == "online":
                return True
    return False

def mister_json_parserson(json_path: str) -> dict:
    f = None
    # check input parameter, it must be a json file.
    split = str(json_path).split(".")
    file_type = split[split.__len__() - 1]
    if file_type != "json":
        raise Exception("File type must be json")
    try:
        f = open(json_path)
    except FileNotFoundError:
        print(f"A json file {json_path} does not exist")
    # load json
    with f as fo:
        k = mKvList.KeyValueList(json.load(fo))
        return k

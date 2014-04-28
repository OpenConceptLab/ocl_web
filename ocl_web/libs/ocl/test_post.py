from libs.ocl import Org

def do_it(**kwargs):

    org_id = kwargs.pop('org_id')
    name = kwargs.pop('name')
    return Org.create(org_id, name, **kwargs)

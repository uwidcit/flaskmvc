from App.models import Provider
from App.database import db

def create_provider(provider_id, provider_name, contact_info):
    new_provider = Provider(provider_id=provider_id, provider_name=provider_name, contact_info=contact_info)
    db.session.add(new_provider)
    db.session.commit()
    return new_provider

def get_provider(provider_id):
    return Provider.query.get(provider_id)

def get_provider_by_contact(contact_info):
    return Provider.query.filter_by(contact_info=contact_info).first()

def get_all_providers():
    return Provider.query.all()

def get_all_provider_json():
    providers=get_all_providers()
    if not providers: return None
    providers = [provider.get_json() for provider in providers]
    return providers

def update_provider(provider_id, provider_name, contact_info):
    provider = get_provider(provider_id)
    if not provider: return None
    provider.provider_name = provider_name
    provider.contact_info = contact_info
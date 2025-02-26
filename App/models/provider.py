from App.database import db

class Provider(db.model):
    provider_id = db.Column(db.String(30), primary_key=True)
    provider_name = db.Column(db.String(30), nullable=False)
    contact_info = db.Column(db.String(30), nullable=False)
    
def __init__(self, provider_id, provider_name, contact_info):
    self.provider_id=provider_id
    self.provider_name=provider_name
    self.contact_info = contact_info
    
def get_json(self):
    return{
        'provider_id':self.provider_id,
        'provider_name':self.provider_name,
        'provider_contact':self.contact_info
    }
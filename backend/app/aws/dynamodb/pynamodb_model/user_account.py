from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

from backend.app.global_settings import global_settings

class UserAccount(Model):
    class Meta:
        table_name = f"grind-meter-{global_settings.STAGE}-user-account"
        region = global_settings.REGION

    user_id = UnicodeAttribute(hash_key=True)
    monday = UnicodeAttribute(null=True)
    tuesday = UnicodeAttribute(null=True)
    wednesday = UnicodeAttribute(null=True)
    thursday = UnicodeAttribute(null=True)
    friday = UnicodeAttribute(null=True)
    saturday = UnicodeAttribute(null=True)
    sunday = UnicodeAttribute(null=True)


from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

from backend.app.global_settings import global_settings

class UserPlanUserId(GlobalSecondaryIndex):
    class Meta:
        index_name = 'user_id'
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()

    user_id = UnicodeAttribute(hash_key=True)
class UserPlan(Model):
    class Meta:
        table_name = f"grind-meter-{global_settings.STAGE}-user-plan"
        region = global_settings.REGION

    user_id = UnicodeAttribute(range_key=True)
    plan_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    plan_state = UnicodeAttribute()

    user_id_index = UserPlanUserId()

from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute, MapAttribute, NumberAttribute

from backend.app.global_settings import global_settings

class ExerciseSetMap(MapAttribute):
    repetitions = NumberAttribute()
    mass = NumberAttribute()
    unit = UnicodeAttribute()
    index = NumberAttribute()


class UserExerciseReport(Model):
    class Meta:
        table_name = f"grind-meter-{global_settings.STAGE}-user-exercise-report"
        region = global_settings.REGION

    exercise_id = UnicodeAttribute(hash_key=True)
    timestamp = NumberAttribute(range_key=True)
    report_id = UnicodeAttribute()
    exercise_sets = ListAttribute(of=ExerciseSetMap)

import uuid
from datetime import datetime, timedelta

from backend.app.aws.dynamodb.pynamodb_model.user_exercise_report import UserExerciseReport, ExerciseSetMap
from backend.app.enum.weight_unit import WeightUnit
from backend.app.schemas.exercise_set import ExerciseSet
from backend.app.schemas.lift_exercise_report import LiftExerciseReport
from backend.app.schemas.weight import Weight


class UserExerciseReportController:
    def add_lift_exercise_report(self, user_exercise_report: LiftExerciseReport, user: str):
        exercise_sets = []
        for single_set in user_exercise_report.sets:
            if single_set.weight.unit == WeightUnit.KG.value:
                mass = single_set.weight.mass * 1000
                weight_unit = WeightUnit.G.value
                exercise_sets.append(ExerciseSetMap(
                    repetitions=single_set.repetitions,
                    mass=mass,
                    unit=weight_unit,
                    index=single_set.index
                ))
                continue

            raise NotImplementedError("Weight unit not supported!")

        report_id = str(uuid.uuid4())
        user_exercise_report = UserExerciseReport(
            exercise_id=user_exercise_report.exercise.id,
            timestamp=user_exercise_report.timestamp,
            report_id=report_id,
            exercise_sets=exercise_sets
        )

        user_exercise_report.save()

        return report_id

    def get_last_report(self, user_id: str, exercise_id: str):
        for item in UserExerciseReport.query(
            exercise_id,
            limit=1,
            scan_index_forward=False
        ):
            sets = []
            #TODO check if user_id is the same or allow for every logged user to see it. Now its visible
            for single_set in item.exercise_sets:
                if single_set.unit == WeightUnit.G.value:
                    sets.append(ExerciseSet(
                        repetitions=single_set.repetitions,
                        weight=Weight(unit=WeightUnit.KG.value, mass=single_set.mass/1000),
                        index=single_set.index))
                    continue
                raise NotImplementedError("Weight unit not supported!")

            return LiftExerciseReport(sets=sets)

        return None

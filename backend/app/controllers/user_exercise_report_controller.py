import uuid
from datetime import datetime, timedelta

from backend.app.aws.dynamodb.pynamodb_model.user_exercise import UserExercise
from backend.app.aws.dynamodb.pynamodb_model.user_exercise_report import UserExerciseReport, ExerciseSetMap
from backend.app.enum.weight_unit import WeightUnit
from backend.app.schemas.exercise import Exercise
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

    def get_last_report(self, user_id: str, exercise_id: str, count: int):
        max_count = 2

        if count > max_count:
            raise ValueError(f"Max count of reports is:{max_count}")

        exercise = UserExercise().get(exercise_id, user_id)

        item_list = []

        for item in UserExerciseReport.query(
                exercise_id,
                limit=count,
                scan_index_forward=False
        ):
            sets = []
            for single_set in item.exercise_sets:
                if single_set.unit == WeightUnit.G.value:
                    sets.append(ExerciseSet(
                        repetitions=single_set.repetitions,
                        weight=Weight(unit=WeightUnit.KG.value, mass=single_set.mass / 1000),
                        index=single_set.index))
                    continue
                raise NotImplementedError("Weight unit not supported!")

            item_list.append(LiftExerciseReport(
                sets=sets,
                exercise=Exercise(
                    id=exercise.exercise_id,
                    name=exercise.name,
                    type=exercise.type),
                timestamp=item.timestamp
            ))

        return item_list

    def get_reports(self, user_id: str, exercise_id: str, page: int):
        max_count = 1

        if page > max_count:
            raise ValueError(f"current max page:{max_count}")

        exercise = UserExercise().get(exercise_id, user_id)

        item_list = []

        for item in UserExerciseReport.query(
                exercise_id,
                limit=25,
                scan_index_forward=False
        ):
            sets = []
            for single_set in item.exercise_sets:
                if single_set.unit == WeightUnit.G.value:
                    sets.append(ExerciseSet(
                        repetitions=single_set.repetitions,
                        weight=Weight(unit=WeightUnit.KG.value, mass=single_set.mass / 1000),
                        index=single_set.index))
                    continue
                raise NotImplementedError("Weight unit not supported!")

            item_list.append(LiftExerciseReport(
                sets=sets,
                exercise=Exercise(
                    id=exercise.exercise_id,
                    name=exercise.name,
                    type=exercise.type,
                    state=exercise.exercise_state),
                timestamp=item.timestamp
            ))

        return item_list

from backend.app.aws.dynamodb.pynamodb_model.user_exercise_report import UserExerciseReport
from backend.app.enum.weight_unit import MeasureUnit
from backend.app.schemas.exercise_set import ExerciseSet
from backend.app.schemas.lift_exercise_report import LiftExerciseReport
from backend.app.schemas.weight import Weight


class ReportService:
    def get_report_from_db_item(self, item: UserExerciseReport) -> LiftExerciseReport:
        sets = []

        for single_set in item.exercise_sets:
            if single_set.unit == MeasureUnit.G.value:
                sets.append(ExerciseSet(
                    repetitions=single_set.repetitions,
                    weight=Weight(unit=MeasureUnit.KG.value, mass=single_set.mass / 1000),
                    index=single_set.index))
                continue
            raise NotImplementedError("Weight unit not supported!")

        return LiftExerciseReport(
            exerciseId=item.exercise_id,
            reportId=item.report_id,
            sets=sets,
            timestamp=item.timestamp
        )

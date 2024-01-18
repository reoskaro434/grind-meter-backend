import uuid
from datetime import datetime

from fastapi import HTTPException
from pynamodb.exceptions import DoesNotExist

from backend.app.aws.dynamodb.pynamodb_model.user_exercise import UserExercise
from backend.app.aws.dynamodb.pynamodb_model.user_exercise_report import UserExerciseReport, ExerciseSetMap
from backend.app.enum.weight_unit import MeasureUnit
from backend.app.schemas.lift_exercise_report import LiftExerciseReport
from backend.app.services.report_service import ReportService
from fastapi.responses import StreamingResponse
import csv
import io


class UserExerciseReportController:
    def __init__(self):
        self.report_service = ReportService()

    def __get_exercise_if_user_valid(self, exercise_id: str, user_id: str) -> UserExercise:
        try:
            exercise = UserExercise().get(exercise_id, user_id)  # Validates user owns exercise

            return exercise
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Report not found")

    def add_lift_exercise_report(self, user_exercise_report: LiftExerciseReport, user: str):
        exercise_sets = []
        for single_set in user_exercise_report.sets:
            if single_set.weight.unit == MeasureUnit.KG.value:
                mass = single_set.weight.mass * 1000
                weight_unit = MeasureUnit.G.value
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
            exercise_id=user_exercise_report.exercise_id,
            timestamp=user_exercise_report.timestamp,
            report_id=report_id,
            exercise_sets=exercise_sets
        )

        user_exercise_report.save()

        return report_id

    def get_last_report(self, user_id: str, exercise_id: str, count: int):
        max_count = 2

        if count > max_count:
            raise ValueError(f"Max count of reports is:{max_count}")  # Temporary solution

        self.__get_exercise_if_user_valid(exercise_id, user_id)  # Validates user owns exercise

        item_list = []

        for item in UserExerciseReport.query(
                exercise_id,
                limit=count,
                scan_index_forward=False
        ):
            lift_exercise_rep: LiftExerciseReport = self.report_service.get_report_from_db_item(item)

            item_list.append({
                "reportId": lift_exercise_rep.report_id,
                "exerciseId": lift_exercise_rep.exercise_id,
                "sets": lift_exercise_rep.sets,
                "timestamp": lift_exercise_rep.timestamp
            })

        return item_list

    def get_report(self, user_id: str, exercise_id: str, timestamp: int):
        exercise = self.__get_exercise_if_user_valid(user_id, exercise_id)

        db_item = UserExerciseReport.get(exercise.exercise_id, timestamp)

        lift_exercise_report = self.report_service.get_report_from_db_item(db_item)

        return {
            "reportId": lift_exercise_report.report_id,
            "exerciseId": lift_exercise_report.exercise_id,
            "sets": lift_exercise_report.sets,
            "timestamp": lift_exercise_report.timestamp
        }

    def get_reports(self, user_id: str, exercise_id: str, page: int):
        self.__get_exercise_if_user_valid(exercise_id, user_id)  # Validates user owns exercise

        item_list = []

        for item in UserExerciseReport.query(
                exercise_id,
                limit=25,
                scan_index_forward=False
        ):
            lift_exercise_report: LiftExerciseReport = self.report_service.get_report_from_db_item(item)

            item_list.append({
                "reportId": lift_exercise_report.report_id,
                "exerciseId": lift_exercise_report.exercise_id,
                "sets": lift_exercise_report.sets,
                "timestamp": lift_exercise_report.timestamp
            })

        return item_list

    def get_reports_from_range(self, user_id: str, exercise_id: str, start: int, end: int) -> list[LiftExerciseReport]:
        self.__get_exercise_if_user_valid(exercise_id, user_id)  # Validates user owns exercise

        item_list = []

        for item in UserExerciseReport.query(
                exercise_id,
                range_key_condition=(UserExerciseReport.timestamp.between(start, end)),
                scan_index_forward=False
        ):
            lift_exercise_report: LiftExerciseReport = self.report_service.get_report_from_db_item(item)

            item_list.append(lift_exercise_report)

        return item_list

    def delete(self, user_id: str, exercise_id: str, timestamp: int):
        self.__get_exercise_if_user_valid(exercise_id, user_id)

        try:
            db_item = UserExerciseReport.get(exercise_id, timestamp)
            db_item.delete()
        except DoesNotExist:
            pass

        return True

    def download_csv_report(self, user_id: str, exercise_id: str, start: int, end: int):
        report_list: list[LiftExerciseReport] = self.get_reports_from_range(user_id, exercise_id, start, end)

        csv_report = [
            ["timestamp", "date", "repetitions", "weight", "unit", "index"]
        ]

        for report in report_list:
            exercise_date = datetime.fromtimestamp(int(report.timestamp) // 1000).strftime("%Y-%m-%d")

            for single_set in report.sets:
                record = [
                    report.timestamp,
                    exercise_date,
                    single_set.repetitions,
                    single_set.weight.mass,
                    single_set.weight.unit,
                    single_set.index
                ]

                csv_report.append(record)

        stream = io.StringIO()
        csv_writer = csv.writer(stream)
        csv_writer.writerows(csv_report)
        stream.seek(0)

        response = StreamingResponse(iter([stream.read()]), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"

        return response

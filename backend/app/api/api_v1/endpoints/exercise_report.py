from fastapi import APIRouter
from backend.app.api.deps import UserDep
from backend.app.controllers.user_exercise_report_controller import UserExerciseReportController
from backend.app.schemas.lift_exercise_report import LiftExerciseReport

router = APIRouter()


@router.post('/add-lift-report')
async def add_lift_report(lift_exercise_report: LiftExerciseReport, user: UserDep):
    return UserExerciseReportController().add_lift_exercise_report(lift_exercise_report, user.email)

@router.get('/get-last-report/{exercise_id}/{count}')
async def get_last_report(user: UserDep, exercise_id: str, count: int):
    return UserExerciseReportController().get_last_report(user.email, exercise_id, count)

@router.get('/get-report/{exercise_id}/{timestamp}')
async def get_last_report(user: UserDep, exercise_id: str, timestamp: int):
    return UserExerciseReportController().get_report(user.email, exercise_id, timestamp)
@router.get('/get-reports/{exercise_id}/{page}')
async def get_reports(user: UserDep, exercise_id: str, page: int):
    return UserExerciseReportController().get_reports(user.email, exercise_id, page)
@router.get('/get-reports-from-range/{exercise_id}/{start}/{end}')
async def get_reports_from_range(user: UserDep, exercise_id: str, start: int, end: int):
    report_list = UserExerciseReportController().get_reports_from_range(user.email, exercise_id, start, end)

    camel_report_list = []

    for report in report_list:
        camel_report_list.append({
            "reportId": report.report_id,
            "exerciseId": report.exercise_id,
            "sets": report.sets,
            "timestamp": report.timestamp
        })

    return camel_report_list

@router.get('/download-csv-report/{exercise_id}/{start}/{end}')
async def download_csv_report(user: UserDep, exercise_id: str, start: int, end: int):
    return UserExerciseReportController().download_csv_report(user.email, exercise_id, start, end)
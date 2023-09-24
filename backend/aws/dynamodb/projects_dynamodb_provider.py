import calendar
import datetime
import uuid

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from backend.aws.dynamodb.base_dynamodb_provider import BaseDynamodbProvider


class ProjectsDynamodbProvider(BaseDynamodbProvider):
    def __init__(self, region, stage):
        super().__init__(f"perfect-projects-{stage}-{region}-projects")

    def add_project(self, project):
        item_id = str(uuid.uuid4())
        current_datetime = datetime.datetime.utcnow()
        current_timetuple = current_datetime.utctimetuple()
        current_timestamp = calendar.timegm(current_timetuple)
        item = {
            "id": item_id,
            "user_id": project.get("author").lower(),
            "title": project.get("title"),
            "brief_description": project.get("briefDescription"),
            "visible": project.get("visible"),
            "last_timestamp": current_timestamp
        }
        try:
            self.table.put_item(Item=item)
        except ClientError as error:
            print(error)
            return False
        return item_id

    def get_all_user_projects(self, user_id):
        try:
            result = self.table.query(IndexName="user_id",
                                      KeyConditionExpression=Key("user_id").eq(user_id))
        except ClientError as error:
            print(error)
            return False
        return result

    def delete_project(self, project_id):
        try:
            self.table.delete_item(Key={"id": project_id})
        except ClientError as error:
            print(error)
            return False
        return True

    def get_project(self, project_id):
        try:
            item = self.table.get_item(Key={"id": project_id})
        except ClientError as error:
            print(error)
            return False
        return item

    def get_projects(self, page):
        limit = 3
        try:
            response = self.table.scan(Limit=limit)
            for x in range(page - 1):
                last_evaluated_key = response.get("LastEvaluatedKey")
                if last_evaluated_key is None:
                    break
                response = self.table.scan(Limit=limit, ExclusiveStartKey=response.get("LastEvaluatedKey"))
            items = response.get("Items")
        except ClientError as error:
            print(error)
            return False
        return items

    def update_project(self, project_data):
        current_datetime = datetime.datetime.utcnow()
        current_timetuple = current_datetime.utctimetuple()
        current_timestamp = calendar.timegm(current_timetuple)
        try:
            self.table.update_item(
                Key={"id": project_data.get("id")},
                UpdateExpression="set visible=:visible, brief_description=:brief_description, "
                                 "last_timestamp=:last_timestamp, "
                                 "title=:title",
                ExpressionAttributeValues={
                    ":visible": project_data.get("visible"),
                    ":brief_description": project_data.get("briefDescription"),
                    ":last_timestamp": current_timestamp,
                    ":title": project_data.get("title"),
                })
        except ClientError as error:
            print(error)
            return False
        return True

    def update_visibility(self, project_id, visible):
        try:
            self.table.update_item(
                Key={"id": project_id},
                UpdateExpression="set visible=:visible",
                ExpressionAttributeValues={
                    ":visible": visible
                })
        except ClientError as error:
            print(error)
            return False
        return True

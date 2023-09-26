from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from backend.app.aws.dynamodb.base_dynamodb_provider import BaseDynamodbProvider


class SavedProjectsDynamodbProvider(BaseDynamodbProvider):
    def __init__(self, region, stage):
        super().__init__(f"perfect-projects-{stage}-{region}-saved-projects")

    def save_project(self, user_id, project_id):
        item = {
            "project_id": project_id,
            "user_id": user_id
        }
        try:
            self.table.put_item(Item=item)
        except ClientError as error:
            print(error)
            return False
        return True

    def delete_save(self, user_id, project_id):
        try:
            self.table.delete_item(Key={"user_id": user_id, "project_id": project_id})
        except ClientError as error:
            print(error)
            return False
        return True

    def get_saved_projects(self, user_id):
        try:
            result = self.table.query(IndexName="user_id",
                                      KeyConditionExpression=Key("user_id").eq(user_id))
        except ClientError as error:
            print(error)
            return False
        return result

    def count_saves(self, project_id):
        try:
            result = self.table.query(IndexName="project_id",
                                      KeyConditionExpression=Key("project_id").eq(project_id))
        except ClientError as error:
            print(error)
            return False
        return int(result.get("Count"))

    def is_saved(self, user_id, project_id):
        try:
            result = self.table.get_item(Key={"user_id": user_id, "project_id": project_id})
        except ClientError as error:
            print(error)
            return False
        if result.get("Item"):
            return True
        return False

    def delete_all_project_saves(self, project_id):
        try:
            result = self.table.query(IndexName="project_id",
                                      KeyConditionExpression=Key("project_id").eq(project_id))
            items = result.get("Items")
            for item in items:
                self.delete_save(item.get("user_id"), item.get("project_id"))
        except ClientError as error:
            print(error)
            return False
        return True

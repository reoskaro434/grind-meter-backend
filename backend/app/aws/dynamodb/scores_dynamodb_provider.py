from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from backend.app.aws.dynamodb.base_dynamodb_provider import BaseDynamodbProvider


class ScoresDynamodbProvider(BaseDynamodbProvider):
    def __init__(self, region, stage):
        super().__init__(f"perfect-projects-{stage}-{region}-scores")

    def add_score(self, user_id, project_id):
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

    def delete_score(self, user_id, project_id):
        try:
            self.table.delete_item(Key={"user_id": user_id, "project_id": project_id})
        except ClientError as error:
            print(error)
            return False
        return True

    def count_scores(self, project_id):
        try:
            result = self.table.query(IndexName="project_id",
                                      KeyConditionExpression=Key("project_id").eq(project_id))
        except ClientError as error:
            print(error)
            return False
        return int(result.get("Count"))

    def is_scored(self, user_id, project_id):
        try:
            result = self.table.get_item(Key={"user_id": user_id, "project_id": project_id})
        except ClientError as error:
            print(error)
            return False
        if result.get("Item"):
            return True
        return False

    def delete_all_project_scores(self, project_id):
        try:
            result = self.table.query(IndexName="project_id",
                                      KeyConditionExpression=Key("project_id").eq(project_id))
            items = result.get("Items")
            for item in items:
                self.delete_score(item.get("user_id"), item.get("project_id"))
        except ClientError as error:
            print(error)
            return False
        return True

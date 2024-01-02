from fastapi import HTTPException
from pynamodb.exceptions import DoesNotExist

from backend.app.aws.dynamodb.pynamodb_model.user_account import UserAccount
from backend.app.schemas.account import Account


class AccountController:
    def update(self, account: Account, email):
        if account.user_id != email:
            raise HTTPException(status_code=403, detail="You are not the owner of this plan")

        try:
            user_account = UserAccount.get(account.user_id)
        except DoesNotExist:
            user_account = UserAccount(
                user_id=account.user_id
            )
            user_account.save()

        user_account.update(actions=[
            UserAccount.monday.set(account.monday),
            UserAccount.tuesday.set(account.tuesday),
            UserAccount.wednesday.set(account.wednesday),
            UserAccount.thursday.set(account.thursday),
            UserAccount.friday.set(account.friday),
            UserAccount.saturday.set(account.saturday),
            UserAccount.sunday.set(account.sunday)
        ])

        return True

    def get_account(self, email: str) -> dict:
        try:
            user_account = UserAccount.get(email)
        except DoesNotExist:
            return {
                "userId": email,
                "monday": "",
                "tuesday": "",
                "wednesday": "",
                "thursday": "",
                "friday": "",
                "saturday": "",
                "sunday": ""
            }

        return {
            "userId": user_account.user_id,
            "monday": user_account.monday,
            "tuesday": user_account.tuesday,
            "wednesday": user_account.wednesday,
            "thursday": user_account.thursday,
            "friday": user_account.friday,
            "saturday": user_account.saturday,
            "sunday": user_account.sunday
        }

    def delete(self, email: str):
        raise NotImplementedError('delete account not implemented')

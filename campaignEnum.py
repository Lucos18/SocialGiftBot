from enum import Enum


class Campaign(Enum):
    FOLLOW = {
        "textMessageToEvaluate": "Segui",
        "timeToWaitBeforeConfirmingCampaign": 20
    }  # TODO to be changed
    LIKE = {
        "textMessageToEvaluate": "Metti LIKE al post",
        "timeToWaitBeforeConfirmingCampaign": 12
    }  # TODO to be changed
    COMMENTS = {
        "textMessageToEvaluate": "COMMENTA il Post"

    }  # TODO to be changed
    STORIES = {
        "textMessageToEvaluate": "Visualizza Le STORIES"

    }  # TODO to be changed
    IGTV = {
        "textMessageToEvaluate": "IGTV",
        "timeToWaitBeforeConfirmingCampaign": 20
    }
    YOUTUBE = {
        "textMessageToEvaluate": "Guarda il video",
        "timeToWaitBeforeConfirmingCampaign": 840  # 14 Minutes
    }  # TODO to be changed
    RULES = {
        "textMessageToEvaluate": "REGOLAMENTO"

    }
    COMPLETED = {
        "textMessageToEvaluate": "Riprova più tardi"

    }


from enum import Enum


class Campaign(Enum):
    FOLLOW = {
        "textMessageToEvaluate": "Segui il profilo"

    }  # TODO to be changed
    LIKE = {
        "textMessageToEvaluate": "Metti LIKE al post"

    }  # TODO to be changed
    COMMENTS = {
        "textMessageToEvaluate": "COMMENTA il Post"

    }  # TODO to be changed
    STORIES = {
        "textMessageToEvaluate": "Visualizza Le STORIES"

    }  # TODO to be changed
    IGTV = {
        "textMessageToEvaluate": "IGTV"
        
    }
    YOUTUBE = {
        "textMessageToEvaluate": "Guarda il video"
        
    }   # TODO to be changed


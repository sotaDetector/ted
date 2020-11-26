import uuid


class randomUtils:

    @staticmethod
    def getRandomStr():
        return str(uuid.uuid4())

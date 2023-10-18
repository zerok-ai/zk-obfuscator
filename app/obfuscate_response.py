class Payload:
    def __init__(self, data):
        self.data = data


class ObfuscateResponse:
    def __init__(self, data):
        self.payload = Payload(data)

    def to_dict(self):
        return {
            "payload": {
                "data": self.payload.data
            }
        }

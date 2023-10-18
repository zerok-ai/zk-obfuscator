from typing import Dict


class ObfuscateRequest:
    """
    Obfuscate request data.

    :param req_data: A request dictionary with the following fields:
        text: the text to analyze
        language: the language of the text
    """

    def __init__(self, req_data: Dict):
        self.data = req_data.get("data")
        self.language = req_data.get("language")

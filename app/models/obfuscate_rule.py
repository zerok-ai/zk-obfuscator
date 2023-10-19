from enum import Enum


class AnonymizerOperator(Enum):
    REPLACE = "replace"


class AnalyzerConfig:
    def __init__(self, type: str, pattern: str):
        self.type = type
        self.pattern = pattern


class AnonymizerConfig:
    def __init__(self, operator: AnonymizerOperator, params: dict):
        self.operator = operator
        self.params = params


class ObfuscateRule:
    def __init__(self, id: str, name: str, analyzer: AnalyzerConfig, anonymizer: AnonymizerConfig):
        self.id = id
        self.name = name
        self.analyzer = analyzer
        self.anonymizer = anonymizer

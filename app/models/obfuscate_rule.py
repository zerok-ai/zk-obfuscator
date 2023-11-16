from enum import Enum


class AnonymizerOperator(Enum):
    REPLACE = "replace"


class AnalyzerConfig:
    def __init__(self, atype: str, pattern: str):
        self.atype = atype
        self.pattern = pattern


class AnonymizerConfig:
    def __init__(self, operator: AnonymizerOperator, params: dict):
        self.operator = operator
        self.params = params


class ObfuscateRule:
    def __init__(self, id: str, name: str, analyzer: AnalyzerConfig, anonymizer: AnonymizerConfig, updatedAt: int):
        self.id = id
        self.name = name
        self.analyzer = analyzer
        self.anonymizer = anonymizer
        self.updatedAt = updatedAt

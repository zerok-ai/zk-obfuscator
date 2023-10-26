import logging
import os
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.analyzer_engine import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer import PatternRecognizer
from presidio_anonymizer.entities import OperatorConfig


class PresidioEngine:

    def __init__(self):
        self.logger = logging.getLogger("zk-obfuscator")
        self.logger.setLevel(os.environ.get("LOG_LEVEL", self.logger.level))
        self.logger.info("Starting obfuscator engine")
        self.anonymizerEngine = AnonymizerEngine()
        registry = RecognizerRegistry()
        registry.load_predefined_recognizers()
        self.analyzerEngine = AnalyzerEngine(registry=registry)
        self.operators = {}

    def obfuscateDict(self, data, language):
        results = {}
        for key, value in data.items():
            if isinstance(value, str):
                results[key] = self.obfuscateText(value, language)
            elif isinstance(value, dict):
                results[key] = self.obfuscateDict(value, language)
            elif isinstance(value, list):
                results[key] = self.obfuscateList(value, language)
            else:
                results[key] = value
        return results

    def obfuscateList(self, data, language):
        results = []
        for value in data:
            if isinstance(value, str):
                results.append(self.obfuscateText(value, language))
            elif isinstance(value, dict):
                results.append(self.obfuscateDict(value, language))
            elif isinstance(value, list):
                results.append(self.obfuscateList(value, language))
            else:
                results.append(value)
        return results

    def obfuscateText(self, text, language):
        recognizer_result_list = self.analyzerEngine.analyze(
            text=text,
            language=language,
        )

        print(text, recognizer_result_list)

        anoymizer_result = self.anonymizerEngine.anonymize(
            text=text,
            analyzer_results=recognizer_result_list,
            operators=self.operators,
        )
        return anoymizer_result.text

    def updateObfuscationRules(self, obfuscation_rules):
        registry = RecognizerRegistry()
        registry.load_predefined_recognizers()
        new_operators = {}
        for rule in obfuscation_rules:
            if rule.analyzer.type == "regex":
                rule_name = rule.id + "_" + rule.name
                new_recognizer = PatternRecognizer(supported_entity=rule_name, patterns=[rule.analyzer.pattern])
                registry.add_recognizer(new_recognizer)
                new_config = OperatorConfig("replace", {"new_value": rule.anonymizer.value})
                new_operators[rule_name] = new_config
        newAnalyzerEngine = AnalyzerEngine(registry=registry)
        # Replacing the analyzer engine and operators with the new one.
        self.analyzerEngine = newAnalyzerEngine
        self.operators = new_operators

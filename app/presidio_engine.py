import logging
import os
from presidio_anonymizer import AnonymizerEngine, BatchAnonymizerEngine
from presidio_analyzer.analyzer_engine import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.batch_analyzer_engine import BatchAnalyzerEngine


class PresidioEngine:

    def __init__(self):
        self.logger = logging.getLogger("zk-obfuscator")
        self.logger.setLevel(os.environ.get("LOG_LEVEL", self.logger.level))
        self.logger.info("Starting obfuscator engine")
        self.anonymizerEngine = AnonymizerEngine()
        self.batchAnonymizerEngine = BatchAnonymizerEngine(self.anonymizerEngine)
        registry = RecognizerRegistry()
        registry.load_predefined_recognizers()
        self.analyzerEngine = AnalyzerEngine(registry=registry)
        self.batchAnalyzerEngine = BatchAnalyzerEngine(self.analyzerEngine)

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
            operators={},
        )
        return anoymizer_result.text

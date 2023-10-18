import logging
import os
import json

from flask import Flask, request, jsonify, Response
from werkzeug.exceptions import BadRequest, HTTPException
from presidio_anonymizer.entities import InvalidParamException
from obfuscate_request import ObfuscateRequest
from presidio_engine import PresidioEngine
from obfuscate_response import ObfuscateResponse

DEFAULT_PORT = "9103"


class Server:

    def __init__(self):
        self.logger = logging.getLogger("zk-obfuscator")
        self.logger.setLevel(os.environ.get("LOG_LEVEL", self.logger.level))
        self.app = Flask(__name__)
        self.presidioEngine = PresidioEngine()

        @self.app.route("/healthz")
        def health() -> str:
            return "zk-obfuscator service is up"

        @self.app.route("/obfuscate", methods=["POST"])
        def obfuscate() -> Response:
            try:
                req_data = ObfuscateRequest(request.get_json())
                if not req_data.data:
                    raise Exception("No data provided")

                if not req_data.language:
                    raise Exception("No language provided")

                data = self.presidioEngine.obfuscateDict(req_data.data, req_data.language)
                obfuscateResponse = ObfuscateResponse(data)
                return Response(json.dumps(obfuscateResponse.to_dict()), mimetype="application/json")

            except TypeError as te:
                error_msg = (
                    f"Failed to parse /analyze request "
                    f"for AnalyzerEngine.analyze(). {te.args[0]}"
                )
                self.logger.error(error_msg)
                return jsonify(error=error_msg), 400

            except Exception as e:
                self.logger.error(
                    f"A fatal error occurred during execution of "
                    f"AnalyzerEngine.analyze(). {e}"
                )
                return jsonify(error=e.args[0]), 500

        @self.app.errorhandler(InvalidParamException)
        def invalid_param(err):
            self.logger.warning(
                f"Request failed with parameter validation error: {err.err_msg}"
            )
            return jsonify(error=err.err_msg), 422

        @self.app.errorhandler(HTTPException)
        def http_exception(e):
            return jsonify(error=e.description), e.code

        @self.app.errorhandler(Exception)
        def server_error(e):
            self.logger.error(f"A fatal error occurred during execution: {e}")
            return jsonify(error="Internal server error"), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", DEFAULT_PORT))
    server = Server()
    server.app.run(host="0.0.0.0", port=port)

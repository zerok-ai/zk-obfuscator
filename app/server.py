from fastapi import HTTPException, status, FastAPI
from presidio_anonymizer.entities import InvalidParamException
from models.obfuscate_request import ObfuscateRequest
from models.obfuscate_response import ObfuscateResponse, Payload
from presidio_engine import presidio_engine_obj

app = FastAPI()


@app.get("/healthz")
def health() -> str:
    return "zk-obfuscator service is up"


@app.post("/i/obfuscate", response_model=ObfuscateResponse)
async def obfuscate(request: ObfuscateRequest):
    try:
        if not request.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided")
        if not request.language:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No language provided")

        data = presidio_engine_obj.obfuscateDict(request.data, request.language)
        obfuscateResponse = ObfuscateResponse(payload=Payload(data=data))
        return obfuscateResponse

    except InvalidParamException as err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=err.err_msg)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

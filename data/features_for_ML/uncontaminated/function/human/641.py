from reducto.types import ParseResponse
from reducto.types.shared.parse_response import ParseUsage, ResultFullResult
import httpx

def handle_url_response(response: ParseResponse) -> FullParseResponse:
    if response.result.type == "url":
        with httpx.stream("GET", response.result.url) as r:
            content = r.read().decode()
            result = ResultFullResult.model_validate_json(content)
            return FullParseResponse(
                duration=response.duration,
                job_id=response.job_id,
                result=result,
                usage=response.usage,
            )
    else:
        return FullParseResponse.model_validate(response.model_dump())
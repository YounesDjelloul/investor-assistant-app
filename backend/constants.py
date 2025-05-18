FALLBACK_MESSAGE = (
    "Unfortunately, based on the currently available data, we're unable to provide an answer to your question. "
    "For further assistance, please contact our Investor Relations team at **ir@moove.io**."
)

MODEL_NAME = "gemini-2.0-flash"
RESPONSE_MIME_TYPE = "application/json"
STATUS_NEEDS_CONTEXT = "needs_more_context"
STATUS_NOT_FOUND = "not_found"
FALLBACK_RESPONSE = {"response": FALLBACK_MESSAGE}

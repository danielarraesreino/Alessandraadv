from ninja import Router, Schema

router = Router()

@router.get("/webhook")
def verification(request):
    return {"status": "listening"}


class IncomingMessage(Schema):
    from_number: str
    message_body: str

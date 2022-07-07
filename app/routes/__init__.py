from app import router


class API:
    def __init__(self, *args):
        for ep in args:
            router.include_router(ep.ep)

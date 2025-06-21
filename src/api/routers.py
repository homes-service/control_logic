
from api.v1.instrument_groups import router as router_instrument_groups_v1
from api.v1.auth import router as auth_v1

all_routers = [
    auth_v1,
    router_instrument_groups_v1,
]


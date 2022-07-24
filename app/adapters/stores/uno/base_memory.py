from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class Card(BaseModel):
    class Effects(BaseModel):
        class Kind(str, Enum):
            DRAW = "draw"
            SKIP_TURN = "skip"
            REVERSE_ORDER = "reverse"
            SELECT_COLOR = "select"

        value: Kind
        quantity: int = 1

    color: str
    value: str | int
    img: str = "no_img"
    effect: Effects | None = None


plus_four_effect = Card.Effects(value=Card.Effects.Kind.DRAW, quantity=4)
plus_two_effect = Card.Effects(value=Card.Effects.Kind.DRAW, quantity=2)
turn_skip = Card.Effects(value=Card.Effects.Kind.SKIP_TURN)
reverse = Card.Effects(value=Card.Effects.Kind.REVERSE_ORDER)
select_color = Card.Effects(value=Card.Effects.Kind.SELECT_COLOR)


cards = [
    Card(color="red", value=0),
    Card(color="red", value=1),
    Card(color="red", value=2),
    Card(color="red", value=3),
    Card(color="red", value=4),
    Card(color="red", value=5),
    Card(color="red", value=6),
    Card(color="red", value=7),
    Card(color="red", value=8),
    Card(color="red", value=9),
    Card(color="red", value="+2", effect=plus_two_effect),
    Card(color="red", value="><", effect=reverse),
    Card(color="red", value="X", effect=turn_skip),
    Card(color="red", value=0),
    Card(color="red", value=1),
    Card(color="red", value=2),
    Card(color="red", value=3),
    Card(color="red", value=4),
    Card(color="red", value=5),
    Card(color="red", value=6),
    Card(color="red", value=7),
    Card(color="red", value=8),
    Card(color="red", value=9),
    Card(color="red", value="+2", effect=plus_two_effect),
    Card(color="red", value="><", effect=reverse),
    Card(color="red", value="X", effect=turn_skip),
    ##########
    Card(color="green", value=0),
    Card(color="green", value=1),
    Card(color="green", value=2),
    Card(color="green", value=3),
    Card(color="green", value=4),
    Card(color="green", value=5),
    Card(color="green", value=6),
    Card(color="green", value=7),
    Card(color="green", value=8),
    Card(color="green", value=9),
    Card(color="green", value="+2", effect=plus_two_effect),
    Card(color="green", value="><", effect=reverse),
    Card(color="green", value="X", effect=turn_skip),
    Card(color="green", value=0),
    Card(color="green", value=1),
    Card(color="green", value=2),
    Card(color="green", value=3),
    Card(color="green", value=4),
    Card(color="green", value=5),
    Card(color="green", value=6),
    Card(color="green", value=7),
    Card(color="green", value=8),
    Card(color="green", value=9),
    Card(color="green", value="+2", effect=plus_two_effect),
    Card(color="green", value="><", effect=reverse),
    Card(color="green", value="X", effect=turn_skip),
    ##########
    Card(color="blue", value=0),
    Card(color="blue", value=1),
    Card(color="blue", value=2),
    Card(color="blue", value=3),
    Card(color="blue", value=4),
    Card(color="blue", value=5),
    Card(color="blue", value=6),
    Card(color="blue", value=7),
    Card(color="blue", value=8),
    Card(color="blue", value=9),
    Card(color="blue", value="+2", effect=plus_two_effect),
    Card(color="blue", value="><", effect=reverse),
    Card(color="blue", value="X", effect=turn_skip),
    Card(color="blue", value=0),
    Card(color="blue", value=1),
    Card(color="blue", value=2),
    Card(color="blue", value=3),
    Card(color="blue", value=4),
    Card(color="blue", value=5),
    Card(color="blue", value=6),
    Card(color="blue", value=7),
    Card(color="blue", value=8),
    Card(color="blue", value=9),
    Card(color="blue", value="+2", effect=plus_two_effect),
    Card(color="blue", value="><", effect=reverse),
    Card(color="blue", value="X", effect=turn_skip),
    ##########
    Card(color="yellow", value=0),
    Card(color="yellow", value=1),
    Card(color="yellow", value=2),
    Card(color="yellow", value=3),
    Card(color="yellow", value=4),
    Card(color="yellow", value=5),
    Card(color="yellow", value=6),
    Card(color="yellow", value=7),
    Card(color="yellow", value=8),
    Card(color="yellow", value=9),
    Card(color="yellow", value="+2", effect=plus_two_effect),
    Card(color="yellow", value="><", effect=reverse),
    Card(color="yellow", value="X", effect=turn_skip),
    Card(color="yellow", value=0),
    Card(color="yellow", value=1),
    Card(color="yellow", value=2),
    Card(color="yellow", value=3),
    Card(color="yellow", value=4),
    Card(color="yellow", value=5),
    Card(color="yellow", value=6),
    Card(color="yellow", value=7),
    Card(color="yellow", value=8),
    Card(color="yellow", value=9),
    Card(color="yellow", value="+2", effect=plus_two_effect),
    Card(color="yellow", value="><", effect=reverse),
    Card(color="yellow", value="X", effect=turn_skip),
    ##########
    Card(color="black", value="+4", effect=plus_four_effect),
    Card(color="black", value="+4", effect=plus_four_effect),
    Card(color="black", value="+4", effect=plus_four_effect),
    Card(color="black", value="+4", effect=plus_four_effect),
    Card(color="black", value="COLOR SWAP", effect=select_color),
    Card(color="black", value="COLOR SWAP", effect=select_color),
    Card(color="black", value="COLOR SWAP", effect=select_color),
    Card(color="black", value="COLOR SWAP", effect=select_color),
]

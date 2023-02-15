from abc import ABC

from .renderable import Renderable


class WorldUi(Renderable, ABC):
    def __init__(self, parent: "World", ui_layer_id: str, priority: float = 1):
        super().__init__(parent.game, parent=parent, render_position=(0, 0), priority=priority)
        # Note that priority must be a float value > 0 here, in order to render above the current Room

        self._ui_layer_id = ui_layer_id

    @property
    def ui_layer_id(self) -> str:
        return self._ui_layer_id

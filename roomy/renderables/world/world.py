from pygame import Surface
from managedstate import State
from managedstate.extensions import Registrar
from managedstate.extensions.registrar import PartialQueries

from os import path
from typing import Type, Set

from ...utils import GameEventType
from ...constants import Constants as GameConstants
from ..screen import Screen
from ..userinterfacelayer import UserInterfaceLayer
from .enums import RenderableDataKey
from .room import Room


class World(Screen):
    """
    An optional concrete implementation of Screen, that represents a standard room-based game world.
    Pulls data to populate the game world from the provided state object, using standardised keys
    """

    def __init__(self, game, state: State.with_extensions(Registrar)):
        super().__init__(game, state)
        self.surface = self._copy_surface()  # Invokes overridden method below to generate a surface

        # Registering classes which may appear in the game state and which would be needed inside this class
        self.game.class_registrar.register(**{
            Room.__name__: Room,
        })

        self._current_room = None
        self._interfaces = set()

        initial_ui_ids = self.state.registered_get("initial_ui_ids")
        for ui_layer_id in initial_ui_ids:
            ui_layer_data = self.state.registered_get("ui_layer", [ui_layer_id])

            ui_layer_class: Type[UserInterfaceLayer] = self.game.class_registrar.get(
                ui_layer_data[RenderableDataKey.CLASS]
            )
            ui_layer_args: list = ui_layer_data.get(RenderableDataKey.ARGS, [])
            ui_layer_kwargs: dict = ui_layer_data.get(RenderableDataKey.KWARGS, {})

            self.add_interface(ui_layer_class(
                self, ui_layer_id,
                *ui_layer_args, **ui_layer_kwargs
            ))

    @property
    def current_room(self) -> Room:
        return self._current_room

    @property
    def interfaces(self) -> Set[UserInterfaceLayer]:
        return self._interfaces

    def set_room(self) -> None:
        """
        Checks what room ID the current room should have via the game's state, and if it does not match
        the room ID of the room that is currently active, a new room with the correct room ID is initialised
        and swapped in.

        This method can be manually invoked in order to apply a room change immediately, but this is not strictly
        necessary - when the room ID is changed in the game's state, on the next call to `.update()` this method will be
        automatically invoked.

        This method assumes that any custom Room subclasses listed in the game's state
        have been made available to the game's ClassRegistrar
        """

        state_current_room_id = self.state.registered_get("current_room_id")
        current_room_id = None if self._current_room is None else self._current_room.room_id

        if state_current_room_id == current_room_id:
            return

        with self.game.game_event_handler(GameEventType.CHANGE_ROOM, self._current_room, state_current_room_id):
            old_room = self._current_room

            new_room_data = self.state.registered_get("room", [state_current_room_id])

            new_room_class: Type[Room] = self.game.class_registrar.get(
                new_room_data[RenderableDataKey.CLASS]
            )
            new_room_args: list = new_room_data.get(RenderableDataKey.ARGS, [])
            new_room_kwargs: dict = new_room_data.get(RenderableDataKey.KWARGS, {})

            new_room = new_room_class(
                self, state_current_room_id,
                *new_room_args, **new_room_kwargs
            )
            self._current_room = new_room

            if old_room is not None:
                old_room.parent_recurface = None

    def add_interface(self, interface: UserInterfaceLayer) -> None:
        """
        This method should be manually invoked, for example when opening a menu, in order to add the provided
        user interface layer into the rendering hierarchy. Unlike with `.set_room()`, this method must always be
        manually invoked to change what UI layers are rendered
        """

        if interface in self.interfaces:
            return

        self._interfaces.add(interface)

    def remove_interface(self, interface: UserInterfaceLayer) -> None:
        """
        This method should be manually invoked, for example when closing, in order to remove the provided
        user interface layer from the rendering hierarchy. Unlike with `.set_room()`, this method must always be
        manually invoked to change what UI layers are rendered
        """

        if interface not in self.interfaces:
            return

        self._interfaces.remove(interface)
        interface.parent_recurface = None

    def _update(self, tick_number: int, elapsed_ms: int, input_events: list, *args, **kwargs) -> None:
        super()._update(tick_number, elapsed_ms, input_events, *args, **kwargs)

        self.set_room()

    def _copy_surface(self) -> Surface:
        surface = Surface((self.game.window.get_width(), self.game.window.get_height()))
        surface.fill(GameConstants.COLOURS["dev"])

        return surface

    @staticmethod
    def register_paths(state: State.with_extensions(Registrar)):
        # Rooms
        default_room_data = {
            RenderableDataKey.CLASS: Room.__name__
        }

        state.register_path("current_room_id", ["current_room_id"], [str(None)])

        state.register_path("room", ["rooms", PartialQueries.KEY], [{}, default_room_data])
        state.register_path("room_occupant", ["room_occupants", PartialQueries.KEY], [{}])

        state.register_path(
            "room_occupants_ids",
            ["rooms", PartialQueries.KEY, "occupants_ids"],
            [{}, default_room_data, []]
        )
        state.register_path(
            "room_background_file_path",
            ["rooms", PartialQueries.KEY, "background_file_path"],
            [{}, default_room_data, path.join(f"{Room.__name__}", f"{str(None)}.png")]
        )

        # UI
        state.register_path("initial_ui_ids", ["initial_ui_ids"], [[]])

        state.register_path("ui_layer", ["ui_layers", PartialQueries.KEY], [{}])

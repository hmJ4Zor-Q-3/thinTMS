from abc import abstractmethod, ABC

from flask import Blueprint


class IFlaskRoutes(ABC):
    """
    A contract for an object for adding a set of routes and behavior to a flask server.
    """

    @abstractmethod
    def get_blueprint(self) -> Blueprint:
        """
        Get the blueprint to add these routes to a flask server.
        Returns: the routes blueprint.

        """
        pass

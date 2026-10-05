"""Plugin registration utilities for LyricView."""

from __future__ import annotations

from typing import Any, Callable


class PluginManager:
    def __init__(self) -> None:
        self._plugins: list[Callable[[Any], Any]] = []

    def use(self, plugin: Callable[[Any], Any] | object, *args: Any, **kwargs: Any) -> Any:
        if callable(plugin):
            return plugin(*args, **kwargs)
        if hasattr(plugin, "install"):
            return plugin.install(*args, **kwargs)
        raise TypeError("Plugin must be a callable or provide an install() method")

    def register(self, plugin: Callable[[Any], Any] | object) -> None:
        self._plugins.append(plugin)

    def apply(self, target: Any, *args: Any, **kwargs: Any) -> list[Any]:
        results: list[Any] = []
        for plugin in self._plugins:
            results.append(self.use(plugin, target, *args, **kwargs))
        return results


def install_plugin(target: Any, plugin: Callable[[Any], Any] | object, *args: Any, **kwargs: Any) -> Any:
    manager = getattr(target, "plugin_manager", None)
    if manager is None:
        manager = PluginManager()
        target.plugin_manager = manager
    return manager.use(plugin, target, *args, **kwargs)

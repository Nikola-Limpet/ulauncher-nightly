from pathlib import Path

import gi
import pytest

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402


def test_night_sky_preferences_does_not_recolor_launcher() -> None:
    if not Gtk.init_check()[0]:
        pytest.skip("GTK display required for CSS cascade verification")

    launcher = Gtk.Window()
    entry = Gtk.Entry()
    launcher.add(entry)
    launcher_css = Gtk.CssProvider()
    launcher_css.load_from_data(b"* { background-color: transparent; background-image: none; }")
    for widget in (launcher, entry):
        widget.get_style_context().add_provider(launcher_css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    companion = Gtk.CssProvider()
    path = Path(__file__).parents[2] / "data/themes/Night Sky/preferences.css"
    companion.load_from_path(str(path))
    screen = launcher.get_screen()
    Gtk.StyleContext.add_provider_for_screen(screen, companion, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION + 1)
    try:
        for widget in (launcher, entry):
            color = widget.get_style_context().get_property("background-color", Gtk.StateFlags.NORMAL)
            assert color.alpha == 0, "Preferences must not paint the launcher or its transparent positioning window"
    finally:
        Gtk.StyleContext.remove_provider_for_screen(screen, companion)
        launcher.destroy()

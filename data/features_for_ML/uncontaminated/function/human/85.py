from gi.repository import Gtk, Adw, Gio, Gdk, GLib

def attempt_focus_and_reenable_prev_button():
                    if int(round(self.carousel.get_position())) == 2:
                        if self.model_selector.provider_sidebar.get_realized() and self.model_selector.provider_sidebar.get_mapped():
                            self.model_selector.provider_sidebar.grab_focus()
                    if self.prev_button.is_sensitive():
                        self.prev_button.set_can_focus(True)
                    return GLib.SOURCE_REMOVE
from gi.repository import Gtk, Adw, GLib

def on_download_complete(success, message):
            if success:
                GLib.idle_add(self._refresh_models)
                toast = Adw.Toast(title=f"Downloaded '{model_name}' Successfully", timeout=3)
                self.preferences_dialog.add_toast(toast)
            else:
                button.set_sensitive(True)
                button.set_child(Gtk.Image.new_from_icon_name("folder-download-symbolic"))
                logger.error(f"Download failed: {message}")
                toast = Adw.Toast(title=f"Failed to Download '{model_name}'", timeout=5)
                self.preferences_dialog.add_toast(toast)
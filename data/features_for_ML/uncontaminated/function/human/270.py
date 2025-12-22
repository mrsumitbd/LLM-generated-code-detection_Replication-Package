from gi.repository import Gtk, Adw, GLib, Gdk, Soup, GdkPixbuf, GtkSource, Gio
import json

def on_response(session, result, msg):
            try:
                if msg.get_status() != Soup.Status.OK:
                    raise RuntimeError(f"HTTP error status {msg.get_status()}")

                glib_bytes = session.send_and_read_finish(result)
                raw_bytes = glib_bytes.get_data()
                json_data = raw_bytes.decode('utf-8')
                self.providers_data = json.loads(json_data)
                GLib.idle_add(self._populate_providers_list)
            except Exception as e:
                logger.error(f"Failed to load providers data from {self.PROVIDERS_DATA_URL}: {e}")
                GLib.idle_add(self._show_error_message, f"Failed to load providers: {e}")
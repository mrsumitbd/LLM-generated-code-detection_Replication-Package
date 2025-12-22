from services import perform_olivetin_action

def trigger_action():
            if result := perform_olivetin_action(self.config, msg_cnf, olivetin_config):
                title, message = result
                if not disable_notifications:
                    self._send_message(title, message, msg_cnf)
from . import bridge_manager as bm
import sublime

def _cleanup_orphan_bridges():
    live_window_ids = {w.id() for w in sublime.windows()}
    for wid in [wid for wid in list(bm.bridges) if wid not in live_window_ids and wid != '__global__']:
        bridge = bm.bridges.pop(wid, None)
        if bridge is not None:
            logger.debug('Immediate cleanup of orphaned bridge for window %s', wid)
            bridge.terminate()
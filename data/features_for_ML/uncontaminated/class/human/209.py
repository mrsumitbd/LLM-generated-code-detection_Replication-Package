import asyncio
import logging
from typing import Dict, Any, Optional, Set, Callable, List, Tuple
from datetime import datetime, timedelta
from .context_aggregator import ContextRequest

class RealTimeContextUpdater:
    """Manage real-time context updates during incidents."""
    
    def __init__(self, server_instance=None):
        """Initialize the real-time context updater."""
        self.logger = logging.getLogger(__name__)
        self.server = server_instance
        self.change_detector = ChangeDetector()
        
        # Active monitoring contexts
        self.active_contexts: Dict[str, Dict[str, Any]] = {}
        self.context_snapshots: Dict[str, ContextSnapshot] = {}
        self.monitoring_tasks: Dict[str, asyncio.Task] = {}
        
        # Update intervals based on priority
        self.update_intervals = {
            'critical': 30,    # seconds
            'high': 60,
            'medium': 300,     # 5 minutes
            'low': 900,        # 15 minutes
            'background': 1800 # 30 minutes
        }
        
        # Subscriber management
        self.subscribers: Dict[str, Set[Callable]] = {}
        self.global_subscribers: Set[Callable] = set()
        
        # Statistics
        self.stats = {
            'total_updates': 0,
            'change_events': 0,
            'active_monitors': 0,
            'last_update': None
        }
    
    async def start_monitoring(self, context_id: str, context_type: str, 
                              priority: str = 'medium', initial_context: Optional[Dict[str, Any]] = None) -> None:
        """
        Start monitoring a context for real-time updates.
        
        Args:
            context_id: Unique identifier for the context
            context_type: Type of context (incident, hunting, etc.)
            priority: Update priority level
            initial_context: Initial context data for baseline
        """
        if context_id in self.active_contexts:
            self.logger.warning(f"Context {context_id} is already being monitored")
            return
        
        self.logger.info(f"Starting real-time monitoring for context {context_id} (type: {context_type}, priority: {priority})")
        
        # Initialize context tracking
        self.active_contexts[context_id] = {
            'context_type': context_type,
            'priority': priority,
            'started_at': datetime.utcnow().isoformat(),
            'last_update': datetime.utcnow().isoformat(),
            'update_count': 0,
            'change_count': 0,
            'status': 'active'
        }
        
        # Create initial snapshot if context provided
        if initial_context:
            snapshot = ContextSnapshot.create(context_id, context_type, initial_context)
            self.context_snapshots[context_id] = snapshot
            self.logger.debug(f"Created initial snapshot for {context_id}: {snapshot.checksum}")
        
        # Initialize subscriber list
        if context_id not in self.subscribers:
            self.subscribers[context_id] = set()
        
        # Start monitoring task
        interval = self.update_intervals.get(priority, 300)
        task = asyncio.create_task(self._monitor_context(context_id, interval))
        self.monitoring_tasks[context_id] = task
        
        # Update statistics
        self.stats['active_monitors'] = len(self.active_contexts)
        
        self.logger.info(f"Real-time monitoring started for {context_id} with {interval}s intervals")
    
    async def stop_monitoring(self, context_id: str) -> None:
        """
        Stop monitoring a context.
        
        Args:
            context_id: Context identifier to stop monitoring
        """
        if context_id not in self.active_contexts:
            self.logger.warning(f"Context {context_id} is not being monitored")
            return
        
        self.logger.info(f"Stopping real-time monitoring for context {context_id}")
        
        # Cancel monitoring task
        if context_id in self.monitoring_tasks:
            task = self.monitoring_tasks[context_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.monitoring_tasks[context_id]
        
        # Update context status
        if context_id in self.active_contexts:
            self.active_contexts[context_id]['status'] = 'stopped'
            self.active_contexts[context_id]['stopped_at'] = datetime.utcnow().isoformat()
        
        # Clean up resources
        self.active_contexts.pop(context_id, None)
        self.context_snapshots.pop(context_id, None)
        self.subscribers.pop(context_id, None)
        
        # Update statistics
        self.stats['active_monitors'] = len(self.active_contexts)
        
        self.logger.info(f"Real-time monitoring stopped for {context_id}")
    
    async def update_context(self, context_id: str, new_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update context and detect changes.
        
        Args:
            context_id: Context identifier
            new_context: New context data
            
        Returns:
            Change detection result or None if no monitoring
        """
        if context_id not in self.active_contexts:
            self.logger.debug(f"Context {context_id} is not being monitored, skipping update")
            return None
        
        # Get previous snapshot
        old_snapshot = self.context_snapshots.get(context_id)
        
        # Create new snapshot
        context_info = self.active_contexts[context_id]
        new_snapshot = ContextSnapshot.create(context_id, context_info['context_type'], new_context)
        
        # Check if context actually changed
        if old_snapshot and old_snapshot.checksum == new_snapshot.checksum:
            self.logger.debug(f"No changes detected in context {context_id}")
            return None
        
        # Detect changes
        changes = None
        if old_snapshot:
            changes = self.change_detector.detect_changes(old_snapshot.data, new_context)
            
            if changes and changes.get('total_changes', 0) > 0:
                self.logger.info(f"Detected {changes['total_changes']} changes in context {context_id}: {changes['summary']}")
                
                # Update statistics
                self.stats['change_events'] += changes['total_changes']
                context_info['change_count'] += changes['total_changes']
                
                # Notify subscribers
                await self._notify_subscribers(context_id, changes, new_context)
            else:
                self.logger.debug(f"No significant changes detected in context {context_id}")
        
        # Update snapshot and statistics
        self.context_snapshots[context_id] = new_snapshot
        context_info['last_update'] = datetime.utcnow().isoformat()
        context_info['update_count'] += 1
        self.stats['total_updates'] += 1
        self.stats['last_update'] = datetime.utcnow().isoformat()
        
        return changes
    
    def subscribe_to_updates(self, context_id: str, callback: Callable) -> None:
        """
        Subscribe to updates for a specific context.
        
        Args:
            context_id: Context identifier
            callback: Function to call when updates occur
        """
        if context_id not in self.subscribers:
            self.subscribers[context_id] = set()
        
        self.subscribers[context_id].add(callback)
        self.logger.debug(f"Added subscriber for context {context_id}")
    
    def unsubscribe_from_updates(self, context_id: str, callback: Callable) -> None:
        """
        Unsubscribe from updates for a specific context.
        
        Args:
            context_id: Context identifier
            callback: Function to remove from subscribers
        """
        if context_id in self.subscribers:
            self.subscribers[context_id].discard(callback)
            self.logger.debug(f"Removed subscriber for context {context_id}")
    
    def subscribe_to_all_updates(self, callback: Callable) -> None:
        """
        Subscribe to updates for all contexts.
        
        Args:
            callback: Function to call when any context updates occur
        """
        self.global_subscribers.add(callback)
        self.logger.debug("Added global subscriber")
    
    def unsubscribe_from_all_updates(self, callback: Callable) -> None:
        """
        Unsubscribe from all context updates.
        
        Args:
            callback: Function to remove from global subscribers
        """
        self.global_subscribers.discard(callback)
        self.logger.debug("Removed global subscriber")
    
    async def get_context_status(self, context_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status information for a monitored context.
        
        Args:
            context_id: Context identifier
            
        Returns:
            Status information or None if not monitored
        """
        if context_id not in self.active_contexts:
            return None
        
        context_info = self.active_contexts[context_id].copy()
        
        # Add snapshot information
        if context_id in self.context_snapshots:
            snapshot = self.context_snapshots[context_id]
            context_info['last_snapshot'] = {
                'timestamp': snapshot.timestamp,
                'checksum': snapshot.checksum
            }
        
        # Add subscriber count
        context_info['subscriber_count'] = len(self.subscribers.get(context_id, set()))
        
        return context_info
    
    def get_monitoring_stats(self) -> Dict[str, Any]:
        """
        Get overall monitoring statistics.
        
        Returns:
            Dictionary of monitoring statistics
        """
        return {
            **self.stats,
            'active_contexts': list(self.active_contexts.keys()),
            'total_subscribers': sum(len(subs) for subs in self.subscribers.values()) + len(self.global_subscribers),
            'monitoring_intervals': self.update_intervals
        }
    
    async def _monitor_context(self, context_id: str, interval: int) -> None:
        """
        Background task to monitor a context.
        
        Args:
            context_id: Context identifier
            interval: Update interval in seconds
        """
        self.logger.debug(f"Started background monitoring for {context_id} with {interval}s interval")
        
        try:
            while context_id in self.active_contexts:
                await asyncio.sleep(interval)
                
                if context_id not in self.active_contexts:
                    break
                
                # Gather fresh context if server is available
                if self.server and hasattr(self.server, 'context_aggregator'):
                    try:
                        context_info = self.active_contexts[context_id]
                        context_type = context_info['context_type']
                        
                        # Create a mock request for background monitoring
                        from .context_aggregator import ContextRequest
                        request = ContextRequest(
                            prompt=f"Background monitoring for {context_type}",
                            tool_name="monitoring",
                            arguments={"context_id": context_id}
                        )
                        
                        # Gather fresh context
                        fresh_context = await self.server.context_aggregator._gather_context(request)
                        
                        if fresh_context:
                            await self.update_context(context_id, fresh_context)
                        
                    except Exception as e:
                        self.logger.debug(f"Background context gathering failed for {context_id}: {str(e)}")
                
        except asyncio.CancelledError:
            self.logger.debug(f"Background monitoring cancelled for {context_id}")
            raise
        except Exception as e:
            self.logger.error(f"Background monitoring error for {context_id}: {str(e)}")
    
    async def _notify_subscribers(self, context_id: str, changes: Dict[str, Any], new_context: Dict[str, Any]) -> None:
        """
        Notify subscribers of context changes.
        
        Args:
            context_id: Context identifier
            changes: Detected changes
            new_context: Updated context data
        """
        notification = {
            'context_id': context_id,
            'changes': changes,
            'context': new_context,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Notify context-specific subscribers
        context_subscribers = self.subscribers.get(context_id, set())
        for callback in context_subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(notification)
                else:
                    callback(notification)
            except Exception as e:
                self.logger.error(f"Subscriber callback error for {context_id}: {str(e)}")
        
        # Notify global subscribers
        for callback in self.global_subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(notification)
                else:
                    callback(notification)
            except Exception as e:
                self.logger.error(f"Global subscriber callback error: {str(e)}")
    
    async def cleanup(self) -> None:
        """Clean up all monitoring resources."""
        self.logger.info("Cleaning up real-time context updater")
        
        # Stop all monitoring
        context_ids = list(self.active_contexts.keys())
        for context_id in context_ids:
            await self.stop_monitoring(context_id)
        
        # Clear all subscribers
        self.subscribers.clear()
        self.global_subscribers.clear()
        
        self.logger.info("Real-time context updater cleanup completed")
"""Platform Kernel contracts.

This module exports all lifecycle and registration contracts
that components must implement to integrate with the Platform Kernel.
"""

from jarvis.contracts.lifecycle import LifecycleAware, LifecycleState

__all__ = ["LifecycleAware", "LifecycleState"]
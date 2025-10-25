"""Task orchestration built around APScheduler with LangGraph integration hooks."""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional

try:  # pragma: no cover - optional dependency
    from apscheduler.schedulers.background import BackgroundScheduler
except ImportError:  # pragma: no cover
    BackgroundScheduler = None  # type: ignore

try:  # pragma: no cover - optional dependency
    from langgraph.graph import StateGraph
except ImportError:  # pragma: no cover
    StateGraph = None  # type: ignore


class TaskOrchestrator:
    """Schedule local automation flows and orchestrate agent graphs."""

    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler() if BackgroundScheduler is not None else None
        self.graph: Optional[StateGraph] = None
        if self.scheduler is not None:  # pragma: no cover - runtime behaviour
            self.scheduler.start(paused=True)

    def build_graph(self, graph_builder: Callable[[Any], StateGraph]) -> None:
        if StateGraph is None:
            raise RuntimeError("LangGraph is not installed")
        self.graph = graph_builder(StateGraph)

    def schedule_task(self, func: Callable, trigger: str = "interval", **trigger_args: Any) -> str:
        if self.scheduler is None:  # pragma: no cover
            raise RuntimeError("APScheduler is not installed")
        job = self.scheduler.add_job(func, trigger=trigger, **trigger_args)
        return job.id

    def run_pending(self) -> None:
        if self.scheduler is not None:  # pragma: no cover
            self.scheduler.resume()

    def pause(self) -> None:
        if self.scheduler is not None:  # pragma: no cover
            self.scheduler.pause()

    def status(self) -> Dict[str, Any]:
        jobs = []
        if self.scheduler is not None:  # pragma: no cover
            jobs = [
                {
                    "id": job.id,
                    "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                    "name": job.name,
                }
                for job in self.scheduler.get_jobs()
            ]
        return {
            "scheduler_available": self.scheduler is not None,
            "langgraph_available": StateGraph is not None,
            "jobs": jobs,
        }


__all__ = ["TaskOrchestrator"]

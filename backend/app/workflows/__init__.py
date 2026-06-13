# backend/app/workflows/__init__.py

from app.workflows.complaint_analysis_flow import (
    AgentState,
    complaint_analysis_workflow,
    run_complaint_analysis,
    get_compiled_complaint_analysis_workflow,
)
from app.workflows.resolution_flow import (
    ResolutionState,
    resolution_workflow,
    run_document_generation,
    run_resolution_refresh,
    get_compiled_resolution_workflow,
)

__all__ = [
    "AgentState",
    "complaint_analysis_workflow",
    "run_complaint_analysis",
    "get_compiled_complaint_analysis_workflow",
    "ResolutionState",
    "resolution_workflow",
    "run_document_generation",
    "run_resolution_refresh",
    "get_compiled_resolution_workflow",
]

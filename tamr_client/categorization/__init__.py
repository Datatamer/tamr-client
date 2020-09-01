"""
Tamr - Categorization
See https://docs.tamr.com/docs/overall-workflow-classification
"""
from tamr_client.categorization import project
from tamr_client.categorization._categorization import (
    _apply_feedback_async,
    _update_results_async,
    apply_feedback,
    manual_labels,
    update_results,
    update_unified_dataset,
)

import os
import sys


def _check():
    beta_flag = "TAMR_CLIENT_BETA"
    beta_enabled = "1"
    beta = os.environ.get(beta_flag)

    if beta != beta_enabled:
        msg = (
            f"ERROR: 'tamr_client' package is in BETA, but you do not have the '{beta_flag}' environment variable set to '1'."
            "\n\nHINT: Use 'tamr_unify_client' package instead for non-BETA features"
            f"\nHINT: Set environment variable '{beta_flag}=1' to opt-in to BETA features."
            "\n\nWARNING: Do not rely on BETA features in production workflows."
            " Support from Tamr may be limited."
        )
        print(msg)
        sys.exit(1)

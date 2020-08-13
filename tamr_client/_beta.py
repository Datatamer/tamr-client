import os
import sys


def check():
    env_var = "TAMR_CLIENT_BETA"
    is_beta_enabled = os.environ.get(env_var) == "1"

    if not is_beta_enabled:
        msg = (
            f"ERROR: 'tamr_client' package is in BETA, but you do not have the '{env_var}' environment variable set to '1'."
            "\n\nHINT: For non-BETA features, use only the 'tamr_unify_client' package."
            f"\nHINT: To opt-in to BETA features, set environment variable: '{env_var}=1'."
            "\n\nWARNING: Do not rely on BETA features in production workflows."
            " Support from Tamr may be limited."
        )
        print(msg)
        sys.exit(1)

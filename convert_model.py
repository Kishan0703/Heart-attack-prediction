"""Convert legacy XGBoost binary model to JSON for compatibility with modern xgboost.

Run with a Python environment that has xgboost installed (1.7.x or newer).
Example:
    /Users/kishan/.pyenv/versions/3.12.12/bin/python convert_model.py

This script will create `xgb_model.json` alongside the existing binary model.
"""
import xgboost
import os

BIN_PATH = "xgb_model.bin"
JSON_PATH = "xgb_model.json"

def main():
    if not os.path.exists(BIN_PATH):
        print(f"Binary model not found at {BIN_PATH}")
        return 1

    print(f"Loading binary model from {BIN_PATH}")
    bst = xgboost.Booster()
    bst.load_model(BIN_PATH)

    print(f"Saving JSON model to {JSON_PATH}")
    bst.save_model(JSON_PATH)

    print("Done.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

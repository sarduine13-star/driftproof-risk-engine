#!/usr/bin/env python3
# DriftProof Risk Engine - Drift Verification Script
# Patent Pending: U.S. Provisional Application No. 63/905,582
# Copyright (c) 2025 Stephen A. Arduine
# Licensed under MIT License (see LICENSE file)

def check_response(text: str):
    required = ["classification", "cause", "next action"]
    missing = [r for r in required if r not in text.lower()]
    return missing

if __name__ == "__main__":
    sample = input("Paste output:\n")
    missing = check_response(sample)
    if missing:
        print("DRIFT DETECTED:", missing)
    else:
        print("OK")

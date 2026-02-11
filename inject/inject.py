#!/usr/bin/env python3
# DriftProof Risk Engine - Variable Injection Script
# Patent Pending: U.S. Provisional Application No. 63/905,582
# Copyright (c) 2025 Stephen A. Arduine
# Licensed under MIT License (see LICENSE file)

from pathlib import Path
import json
base = Path("prompt/core_prompt.txt").read_text()
vars = json.loads(Path("inject/variables.json").read_text())
for k, v in vars.items():
    base = base.replace(f"{{{{{k}}}}}", v)
print(base)

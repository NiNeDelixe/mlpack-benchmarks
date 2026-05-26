#!/usr/bin/env python3
"""Cross-platform benchmark task runner (Windows-friendly alternative to Makefile)."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _run(cmd, cwd=None, env=None):
    print("[CMD]", " ".join(cmd))
    subprocess.check_call(cmd, cwd=str(cwd or ROOT), env=env)


def _python_bin():
    return sys.executable or "python"


def build_env():
    env = os.environ.copy()
    root = str(ROOT)
    lib = str(ROOT / "libraries" / "lib")
    inc = str(ROOT / "libraries" / "include")
    binp = str(ROOT / "libraries" / "bin")
    share = str(ROOT / "libraries" / "share")
    env["ROOTPATH"] = root
    env["INCLUDEPATH"] = inc
    env["LIBPATH"] = lib
    env["BINPATH"] = binp
    env["JAVAPATH"] = share

    pyver = f"python{sys.version_info.major}.{sys.version_info.minor}"
    site1 = str(ROOT / "libraries" / "lib" / pyver / "site-packages")
    site2 = str(ROOT / "libraries" / "lib" / pyver / "dist-packages")
    env["PYTHONPATH"] = os.pathsep.join([p for p in [env.get("PYTHONPATH", ""), site1, site2] if p])

    if os.name == "nt":
        env["PATH"] = os.pathsep.join([binp, env.get("PATH", "")])
    else:
        env["LD_LIBRARY_PATH"] = os.pathsep.join([env.get("LD_LIBRARY_PATH", ""), lib])

    env["MATLABPATH"] = os.pathsep.join([env.get("MATLABPATH", ""), str(ROOT / "methods" / "matlab")])
    return env


def task_run(args):
    env = build_env()
    cmd = [_python_bin(), "run.py", "-c", args.config, "-o", args.loglevel]
    if args.lib:
        cmd += ["-l", args.lib]
    if args.methods:
        cmd += ["-m", args.methods]
    if args.save:
        cmd += ["-s", args.save]
    _run(cmd, env=env)


def task_setup(args):
    script = "install_all.sh"
    _run(["bash", "download_packages.sh"], cwd=ROOT / "libraries")
    _run(["bash", script, str(args.build_cores)], cwd=ROOT / "libraries")


def task_datasets(_args):
    _run(["bash", "download_datasets.sh"], cwd=ROOT / "datasets")


def main():
    parser = argparse.ArgumentParser(description="Windows-friendly benchmark task runner")
    sub = parser.add_subparsers(dest="task", required=True)

    runp = sub.add_parser("run", help="Run benchmark")
    runp.add_argument("--config", default="test.yaml")
    runp.add_argument("--lib")
    runp.add_argument("--methods")
    runp.add_argument("--save")
    runp.add_argument("--loglevel", default="INFO")
    runp.set_defaults(func=task_run)

    setp = sub.add_parser("setup", help="Download/install libraries")
    setp.add_argument("--build-cores", type=int, default=1)
    setp.set_defaults(func=task_setup)

    datap = sub.add_parser("datasets", help="Download datasets")
    datap.set_defaults(func=task_datasets)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

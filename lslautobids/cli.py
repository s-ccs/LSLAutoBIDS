# lsl_autobids/cli.py

import sys
import runpy

def print_help():
    print("\nUsage: lslautobids <command> [options]\n")
    print("Available commands:")
    print("  gen-proj-config        Generate project config TOML file")
    print("  run               Run AutoBIDS processing pipeline")
    print("  gen-dv-config     Generate Dataverse config")
    print("  help              Show this help message\n")


def main_cli():
    if len(sys.argv) < 2:
        print("Usage: lslautobids <command> [options]\n")
        print_help()
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "help":
        print_help()
        sys.exit(0)

    module_map = {
        'gen-proj-config': 'lslautobids.gen_project_config',
        'run': 'lslautobids.main',
        'gen-dv-config': 'lslautobids.gen_dv_config',
    }

    if command not in module_map:
        print(f"Unknown command: {command}")
        print_help()
        sys.exit(1)

    # Replace sys.argv with new args before running target module
    sys.argv = [command] + args
    runpy.run_module(module_map[command], run_name="__main__")

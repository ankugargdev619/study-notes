import argparse


def create_parser():

    parser = argparse.ArgumentParser(
        prog="tm-cli", description="A command-line task management application"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")

    complete_parser.add_argument("--id", type=int, required=True, help="Task ID")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")

    delete_parser.add_argument("--id", type=int, required=True, help="Task ID")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search tasks")

    search_parser.add_argument("--query", type=str, required=True, help="Search text")

    return parser

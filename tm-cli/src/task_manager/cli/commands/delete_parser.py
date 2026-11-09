def register_delete_parser(subparsers):
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")

    delete_parser.add_argument("--id", type=int, required=True, help="Task ID")

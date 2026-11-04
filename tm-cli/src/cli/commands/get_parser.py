def register_get_parser(subparsers):
    # Get command
    get_parser = subparsers.add_parser("get", help="View a specific task")

    get_parser.add_argument("--id", type=int, required=True, help="Task ID")

def register_list_parser(subparsers):

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")

    list_parser.add_argument(
        "--status",
        choices=["pending", "in_progress", "completed"],
        help="Filter tasks by status",
    )

    list_parser.add_argument(
        "--priority", choices=["low", "medium", "high"], help="Filter tasks by priority"
    )

def register_add_parser(subparsers):

    # Add command
    add_parser = subparsers.add_parser("add", help="Create a new task")

    add_parser.add_argument(
        "--title", type=str, required=True, help="Title of the task"
    )

    add_parser.add_argument(
        "--description", type=str, default="", help="Description of the task"
    )

    add_parser.add_argument(
        "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="Task priority",
    )

    add_parser.add_argument("--due-date", type=str, help="Task due date (YYYY-MM-DD)")

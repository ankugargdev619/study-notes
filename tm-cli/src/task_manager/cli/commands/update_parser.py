def register_update_parser(subparsers):
    # Update command
    update_parser = subparsers.add_parser("update", help="Update an existing task")

    update_parser.add_argument("--id", type=int, required=True, help="Task ID")

    update_parser.add_argument("--title", type=str)
    update_parser.add_argument("--description", type=str)

    update_parser.add_argument("--priority", choices=["low", "medium", "high"])

    update_parser.add_argument("--due-date", type=str)

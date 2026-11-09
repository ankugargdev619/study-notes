def register_complete_parser(subparsers):
    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")

    complete_parser.add_argument("--id", type=int, required=True, help="Task ID")

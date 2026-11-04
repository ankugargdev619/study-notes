def register_search_parser(subparsers):
    # Search command
    search_parser = subparsers.add_parser("search", help="Search tasks")

    search_parser.add_argument("--query", type=str, required=True, help="Search text")

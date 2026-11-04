from task_manager.models.task import Task, Priority
from cli.parser import create_parser


def add_task(args):
    print(f"Creating task: {args.title}")


def list_tasks(args):
    print("Listing tasks")


def delete_task(args):
    print(f"Deleting task: {args.id}")


def complete_task(args):
    print(f"Completing task: {args.id}")


def main():
    parser = create_parser()
    args = parser.parse_args()

    commands = {
        "add": add_task,
        "list": list_tasks,
        "delete": delete_task,
        "complete": complete_task,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()

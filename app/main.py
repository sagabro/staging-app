from app import repositories as repo
from app.utils.init_data import init_data


def main():
    """Main function - creates initial data if it doesn't exist."""
    init_data(repo)


if __name__ == "__main__":
    main()

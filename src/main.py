from src.crawler import crawl_site
from src.indexer import build_index, save_index, load_index
from src.search import print_word, find_query


def main():
    index = None

    print("Search Engine Tool")
    print("Commands: build, load, print <word>, find <query>, exit")

    while True:
        user_input = input("> ").strip()

        if not user_input:
            print("Please enter a command.")
            continue

        parts = user_input.split()
        command = parts[0].lower()
        arguments = parts[1:]

        if command == "exit":
            print("Goodbye.")
            break

        elif command == "build":
            print("Crawling website and building index...")
            pages = crawl_site()
            index = build_index(pages)
            save_index(index)
            print(f"Index built and saved. Pages indexed: {len(pages)}")

        elif command == "load":
            try:
                index = load_index()
                print("Index loaded successfully.")
            except FileNotFoundError as error:
                print(error)

        elif command == "print":
            if index is None:
                print("No index loaded. Run 'build' or 'load' first.")
                continue

            if not arguments:
                print("Usage: print <word>")
                continue

            result = print_word(index, arguments[0])

            if result is None:
                print("Word not found.")
            else:
                print(result)

        elif command == "find":
            if index is None:
                print("No index loaded. Run 'build' or 'load' first.")
                continue

            query = " ".join(arguments)

            if not query:
                print("Usage: find <query>")
                continue

            results = find_query(index, query)

            if not results:
                print("No results found.")
            else:
                for result in results:
                    print(f"{result['url']} | score: {result['score']}")

        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
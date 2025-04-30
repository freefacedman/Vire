from symbiont_core.learner import Learner
from symbiont_core.reflector import Reflector

def launch_cli():
    learner = Learner()
    reflector = Reflector()

    print("\\nWelcome to the Symbiont CLI. Type 'help' for options.\\n")

    loaded_text = None
    summarized_points = None

    while True:
        command = input("Symbiont> ").strip().lower()

        if command == 'help':
            print("Commands:")
            print("  list        - list available inputs")
            print("  load [file] - load a document")
            print("  summarize   - summarize loaded document")
            print("  reflect     - reflect on summarized points")
            print("  exit        - quit CLI")

        elif command == 'list':
            files = learner.list_inputs()
            if not files:
                print("No input files found.")
            else:
                print("Available files:")
                for f in files:
                    print(f"- {f.name}")

        elif command.startswith('load '):
            parts = command.split(' ', 1)
            if len(parts) == 2:
                filename = parts[1]
                loaded_text = learner.load_input(filename)
                if loaded_text:
                    print(f"Loaded file: {filename}")
                else:
                    print("Failed to load file.")
            else:
                print("Usage: load [filename]")

        elif command == 'summarize':
            if loaded_text:
                summarized_points = learner.summarize(loaded_text)
                print("Summary:")
                for idx, point in enumerate(summarized_points, 1):
                    print(f"{idx}. {point}")
            else:
                print("No document loaded.")

        elif command == 'reflect':
            if summarized_points:
                questions = reflector.reflect_on_summary(summarized_points)
                print("Reflection Questions:")
                for q in questions:
                    print(f"- {q}")
            else:
                print("No summary available to reflect on.")

        elif command == 'exit':
            print("Goodbye.")
            break

        else:
            print("Unknown command. Type 'help' for a list.")

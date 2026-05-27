import sys
from time_tracker import TimeTracker

def main():
    tracker = TimeTracker()
    
    if len(sys.argv) < 2:
        print("Usage: time_tracker [start|stop|list] [project_name]")
        return
    
    command = sys.argv[1]
    
    if command == "start":
        if len(sys.argv) < 3:
            print("Please provide a project name.")
            return
        tracker.start_project(sys.argv[2])
    elif command == "stop":
        tracker.stop_project()
    elif command == "list":
        tracker.list_projects()
    else:
        print(f"Unknown command: {command}")
        print("Usage: time_tracker [start|stop|list] [project_name]")

if __name__ == "__main__":
    main()
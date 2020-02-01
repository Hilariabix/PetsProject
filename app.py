import sys
from os import path, walk

from pets import create_app


def get_files_to_watch():
    extra_dirs = ['pets/templates', 'pets/static']
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)
    return extra_files


# run the application
if __name__ == '__main__':
    is_debug = 'debug' in sys.argv
    watch_files = get_files_to_watch()
    app = create_app()
    app.run(debug=is_debug, extra_files=watch_files)
else:
    create_app()

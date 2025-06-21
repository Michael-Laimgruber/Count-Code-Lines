import os
import sys




##############################################################

# INSERT PATH FROM ROOT IN THIS BLOCK
# LIKE THIS: FOLDER_TO_SCAN = r"C:\USERS\USERNAME\PROJECT"


FOLDER_TO_SCAN = r"<FULL - PATH>"
# FOLDER_TO_SCAN = r"C:\USERS\USERNAME\PROJECT" #

##############################################################


EXT_LANGS = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.java': 'Java',
    '.cpp': 'C++',
    '.c': 'C',
    '.cs': 'C#',
    '.html': 'HTML',
    '.css': 'CSS',
    '.json': 'JSON',
    '.xml': 'XML',
    '.php': 'PHP',
}

def is_comment_line(line, ext):
    line = line.strip()
    if not line:
        return False
    if ext == '.py':
        return line.startswith('#')
    elif ext in ['.js', '.ts', '.java', '.cpp', '.c', '.cs', '.php']:
        return line.startswith('//') or line.startswith('/*') or line.startswith('*') or line.endswith('*/')
    elif ext in ['.html', '.xml']:
        return line.startswith('<!--') or line.endswith('-->')
    else:
        return False

# EXCLUDE FOLDERS LIKE GIT AND VENV
EXCLUDED_FOLDERS = {
    '.git', 'venv', '.venv1', '.venv', '__pycache__', 'node_modules',
    'build', 'dist', '.eggs', '.mypy_cache', '.idea,'
}


def count_lines(folder):
    stats = {
        'total_lines': 0,
        'without_comments': 0,
        'without_comments_empty': 0,
        'per_language': {}
    }

    if not os.path.isdir(folder):
        print(f"Error: Folder does not exist: {folder}")
        sys.exit(1)

    for root, dirs, files in os.walk(folder):
        # Remove excluded dirs from traversal
        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERS]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            lang = EXT_LANGS.get(ext)
            if not lang:
                continue

            if lang not in stats['per_language']:
                stats['per_language'][lang] = 0

            full_path = os.path.join(root, file)
            try:
                with open(full_path, encoding='utf-8') as f:
                    lines = f.readlines()
                    stats['total_lines'] += len(lines)

                    for line in lines:
                        if not is_comment_line(line, ext):
                            stats['without_comments'] += 1
                            if line.strip():
                                stats['without_comments_empty'] += 1
                                stats['per_language'][lang] += 1
            except Exception as e:
                print(f"Warning: Could not read file {full_path}: {e}", file=sys.stderr)

    return stats


##############################################################


# OUTPUT FOR TERMINAL

if __name__ == '__main__':
    stats = count_lines(FOLDER_TO_SCAN)

    print("\n" + "=" * 40)
    print("          Code Line Statistics")
    print("=" * 40)
    print(f"{'Total lines:':34}{stats['total_lines']:>6}")
    print(f"{'Lines without comments:':34}{stats['without_comments']:>6}")
    print(f"{'Lines without comments & blanks:':34}{stats['without_comments_empty']:>6}")

    print("\n" + "-" * 40)
    print("Per-language breakdown:")
    print("-" * 40)

    for lang, count in sorted(stats['per_language'].items(), key=lambda x: -x[1]):
        print(f"{lang:<15} : {count:>6}")

    print("=" * 40 + "\n")


##############################################################


# OUTPUT FOR MARKDOWN FORMAT ( e.g. GITHUB README.MD )

if __name__ == '__main__':
    stats = count_lines(FOLDER_TO_SCAN)

    print("\n```markdown")
    print("| Statistic                         |  Lines |")
    print("|:----------------------------------|-------:|")
    print(f"| **Total lines of code**           | {stats['total_lines']:>6} |")
    print(f"| **Lines without comments**        | {stats['without_comments']:>6} |")
    print(f"| **Lines without comments & blanks** | {stats['without_comments_empty']:>6} |")
    print("|\n| Language      |  Lines |")
    print("|:--------------|-------:|")

    for lang, count in sorted(stats['per_language'].items(), key=lambda x: -x[1]):
        print(f"| {lang:<13} | {count:>6} |")

    print("```")

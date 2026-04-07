# /// script
# requires-python = ">=3.10"
# ///
"""Verify that all boxes in an ASCII diagram have consistent line widths.

Usage:
  uv run check_ascii_alignment.py <file>
  echo "diagram" | uv run check_ascii_alignment.py

Checks every box (┌...┐ to └...┘) and reports lines where the right wall
doesn't align with the top-right corner. Handles nested boxes correctly.

The file can be a plain diagram or a markdown file with code blocks.
"""
import sys


def extract_diagrams(text):
    lines = text.split('\n')
    if any(l.strip() == '```' for l in lines):
        return extract_from_markdown(lines)
    return [list(enumerate(lines, 1))]


def extract_from_markdown(lines):
    diagrams = []
    current = []
    in_block = False
    for i, line in enumerate(lines, 1):
        if line.strip() == '```':
            if in_block and current:
                diagrams.append(current)
                current = []
            in_block = not in_block
        elif in_block:
            current.append((i, line))
    return diagrams


def find_boxes(diagram_lines):
    boxes = []
    used_closes = set()
    for i, (line_no, line) in enumerate(diagram_lines):
        for col, ch in enumerate(line):
            if ch == '┌':
                close_col = line.find('┐', col + 1)
                if close_col == -1:
                    continue
                expected_width = close_col - col + 1
                close_line = find_closing_line(diagram_lines, i, col, used_closes)
                if close_line is not None:
                    used_closes.add((close_line, col))
                    boxes.append((line_no, i, col, close_col, close_line))
    return boxes


def find_closing_line(diagram_lines, open_idx, left_col, used_closes):
    for j in range(open_idx + 1, len(diagram_lines)):
        _, line = diagram_lines[j]
        if len(line) > left_col and line[left_col] == '└' and (j, left_col) not in used_closes:
            return j
    return None


def check_box(diagram_lines, open_idx, left_col, right_col, close_idx):
    issues = []
    for j in range(open_idx + 1, close_idx):
        line_no, line = diagram_lines[j]
        if len(line) <= right_col:
            issues.append(
                f"  Line {line_no}: line too short ({len(line)} chars), "
                f"expected '│' at column {right_col} "
                f"(box opened at line {diagram_lines[open_idx][0]})"
            )
        elif line[right_col] != '│':
            issues.append(
                f"  Line {line_no}: expected '│' at column {right_col}, "
                f"found '{line[right_col]}' "
                f"(box opened at line {diagram_lines[open_idx][0]})"
            )
        if line[left_col] != '│':
            issues.append(
                f"  Line {line_no}: expected '│' at column {left_col}, "
                f"found '{line[left_col]}' "
                f"(box opened at line {diagram_lines[open_idx][0]})"
            )
    return issues


def check_text(text):
    diagrams = extract_diagrams(text)
    all_issues = []

    for diagram_lines in diagrams:
        boxes = find_boxes(diagram_lines)
        for line_no, open_idx, left_col, right_col, close_idx in boxes:
            all_issues.extend(
                check_box(diagram_lines, open_idx, left_col, right_col, close_idx)
            )

    if all_issues:
        for issue in all_issues:
            print(issue)
        return 1
    else:
        print("All boxes aligned correctly.")
        return 0


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    sys.exit(check_text(text))

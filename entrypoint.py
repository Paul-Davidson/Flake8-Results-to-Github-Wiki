import git
import json
import os
import sys
from argparse import ArgumentParser


def load_markdown_files(files):
    markdown_dict = {}
    for file in files:
        with open(file, "r") as f:
            markdown_dict["".join(os.path.basename(file).split(".")[:-1])] = \
                f.read()
    return markdown_dict


def generate_markdown(markdown_templates, data):
    content = """
{pie_chart}

\\\\

{top_10_files_by_count}

\\\\

{individual_file_issue_breakdown}
    """.format(
        pie_chart=markdown_templates["pie_chart"],
        top_10_files_by_count=markdown_templates["top_10_files_by_count"],
        individual_file_issue_breakdown=markdown_templates[
            "individual_file_issue_breakdown"
        ],
    )
    return content


def is_git_repo(path):
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False


def is_valid_json(value):
    try:
        json.loads(value)
    except Exception:
        return False
    return True


def main():
    parser = ArgumentParser()
    parser.add_argument("--data", help="flake8 data")
    parser.add_argument("--path-to-wiki-repo", dest="wiki_repo", required=True)
    args = parser.parse_args()

    if not is_git_repo(args.wiki_repo):
        print(
            "Path to wiki repo ({}) is not a valid Git repo."
            .format(args.wiki_repo)
        )
        sys.exit(1)

    print("data provided", args.data)

    if not is_valid_json(args.data):
        print("Data passed in is invalid JSON.")
        sys.exit(1)

    # data = {
    #     ".\\test-files\\bad_file.py": [
    #         {
    #             "code": "F821",
    #             "filename": ".\\test-files\\bad_file.py",
    #             "line_number": 1,
    #             "column_number": 1,
    #             "text": "undefined name 'unicode'",
    #             "physical_line": "unicode\n",
    #         }
    #     ],
    #     ".\\test-files\\good_file.py": [],
    # }

    sorted_files = sorted(
        [(file, issues) for file, issues in args.data.items()],
        key=lambda x: x[0]
    )

    markdown_file_list = [
        "./markdown/pie_chart.md",
        "./markdown/top_10_files_by_count.md",
        "./markdown/individual_file_issue_breakdown.md",
    ]

    markdown_templates = load_markdown_files(markdown_file_list)

    generated_markdown = generate_markdown(markdown_templates, sorted_files)

    print(generated_markdown)

    # if page does not exist - create

    # else update


if __name__ == "__main__":
    main()

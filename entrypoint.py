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


def get_repeated_text_from_markdown(markdown):
    return markdown[
        markdown.index("{r}")+3:
        markdown.rindex("{r}")
    ]


def replace_repeated_text_with_new_text(markdown, new_text):
    return (
        markdown[:markdown.index("{r}")] +
        new_text +
        markdown[markdown.rindex("{r}")+3:]
    )


def generate_pie_chart_data(data):
    return {
        "covered": len([x for x in data if len(x[1]) == 0]),
        "not_covered": len([x for x in data if len(x[1]) > 0]),
    }


def generate_markdown(markdown_templates, data):
    content = """
{pie_chart}

{top_10_files_by_count}

## Individual File Issue Breakdown

{individual_file_issue_breakdown}
    """.strip().format(
        pie_chart=(
            markdown_templates["pie_chart"]
            % generate_pie_chart_data(data)
        ),
        top_10_files_by_count=(
            replace_repeated_text_with_new_text(
                markdown_templates["top_10_files_by_count"],
                "\n".join([
                    get_repeated_text_from_markdown(
                        markdown_templates["top_10_files_by_count"]
                    ) % {
                        "file": file,
                        "count": len(issues)
                    }
                    for file, issues in
                    sorted(data, key=lambda x: len(x[1]))
                    if len(issues) > 0
                ])
            )
        ),
        individual_file_issue_breakdown="\n".join(
            [
                replace_repeated_text_with_new_text(
                    markdown_templates[
                        "individual_file_issue_breakdown"
                    ],
                    "\n".join([
                        get_repeated_text_from_markdown(
                            markdown_templates[
                                "individual_file_issue_breakdown"
                            ]
                        ) % {
                            "line": issue["line_number"],
                            "column": issue["column_number"],
                            "code": issue["code"],
                            "message": issue["text"]
                        }
                        for issue in
                        issues
                    ])
                ) % {
                    "filename": os.path.basename(file),
                    "filepath": file
                }
                for file, issues in
                data
                if len(issues) > 0
            ]
        )
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

    if not is_valid_json(args.data):
        print("Data passed in is invalid JSON.")
        sys.exit(1)

    data = json.loads(args.data)

    sorted_files = sorted(
        [(file, issues) for file, issues in data.items()],
        key=lambda x: x[0]
    )

    markdown_file_list = [
        "./markdown/pie_chart.md",
        "./markdown/top_10_files_by_count.md",
        "./markdown/individual_file_issue_breakdown.md",
    ]

    markdown_templates = load_markdown_files(markdown_file_list)

    generated_markdown = generate_markdown(markdown_templates, sorted_files)

    with open("output.md", "w") as f:
        f.write(generated_markdown)


if __name__ == "__main__":
    main()

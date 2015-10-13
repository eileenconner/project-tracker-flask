from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    return render_template ("student_info.html",
                            first=first,
                            last=last,
                            github=github)

@app.route("/student_search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student_add")
def add_student():
    """Add a student to the database."""

    return render_template("student_add.html")

@app.route("/student_confirmed", methods=['POST'])
def added_student():
    """Confirm a student was added to the database."""

    first = request.form.get('first')
    last = request.form.get('last')
    github = request.form.get('github')

    hackbright.make_new_student(first, last, github)

    return render_template("student_confirmed.html",
                            first=first,
                            last=last,
                            github=github)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)

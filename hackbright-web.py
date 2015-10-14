from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def get_homepage():
    """List all students and all projects on our homepage."""

    list_of_students = hackbright.list_all_students()
    list_of_projects = hackbright.list_all_projects()

    return render_template("index.html",
                            list_of_students=list_of_students,
                            list_of_projects=list_of_projects)

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)


    rows = hackbright.list_projects(github)

    return render_template ("student_info.html",
                            first=first,
                            last=last,
                            github=github,
                            rows=rows
                            )

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

@app.route("/project")
def view_project():
    """List the title, description, and max grade for a given project."""

    project_title = request.args.get('title')

    description, max_grade = hackbright.get_project_info(project_title)

    student_grades = hackbright.list_students_by_completed_project(project_title)

    return render_template("project_info.html",
                            title=project_title,
                            description=description,
                            max_grade=max_grade,
                            student_grades=student_grades)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)

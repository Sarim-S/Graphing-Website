from flask import Flask, render_template
from sympy import symbols, expand, simplify, Eq, solve
from form import VertexForm, ThreePointForm
'''
TO BE ABLE TO RUN THE CODE GO INTO TERMINAL AND TYPE 
pip install -r requirements.txt

AFTER ALL IS INSTALLED, CLICK RUN THEN GO TO THE LINK THAT POPS UP
'''
def format_point(point):
    point = point.replace("(", "").replace(")", "")
    x, y = point.split(",")
    return float(x), float(y)

def solve_three(p1, p2, p3):
    if p1 == p2 or p1 == p3 or p2 == p3:
        message = "Cannot solve this as two points are the same"
        solution = None
        solved = False
        return [message, solution, solved]
    a, b = format_point(p1)
    c, d = format_point(p2)
    e, f = format_point(p3)
    A, B, C = symbols("A B C")
    e1 = Eq(a**2*A + a*B + C, b)
    e2 = Eq(c**2*A + c*B + C, d)
    e3 = Eq(e**2*A + e*B + C, f)
    m_y = max(b,d,f)
    l_y = min(b,d,f)
    farthest_x = max(abs(0-a), abs(0-c), abs(0-e))
    if solve((e1, e2, e3)):
        solutions = solve((e1, e2, e3), rational=True)
        a, b, c = solutions[A], solutions[B], solutions[C]
        message = f"y = {a}x² "
        message += f"+ {b}x " if b >= 0 else f"- {-b}x "
        message += f"+ {c}" if c >= 0 else f"- {-c}"
        solution = f"y = {a}x^2 + {b}x + {c}"
        solved = True
        vertex_form = convert_to_vertex(a, b, c)
    else:
        message = "Those three points cannot make a parabola. Some or all of the points are on the same x or y axis."
        solution = None
        solved = False
        vertex_form = None
    return [message, solution, m_y, l_y, farthest_x, vertex_form, solved]

def convert_to_general(a, p, q):
    A = a
    B = round(p*2*a, 2)
    C = round(p**2*a + q, 2)
    message = f"y = {A}x² "
    message += f"+ {B}x " if B >= 0 else f"- {-B}x"
    message += f"+ {C}" if C >= 0 else f"- {-C}"
    return message

def convert_to_vertex(a, b, c):
    A = a
    try:
        P = round(float((b*-1)/(2*a)), 2) if b != 0 or a != 0 else 0
        Q = round(float(c - (b**2/(4*a))),2) if c != 0 or b != 0 or a != 0 else c
    except:
        P = 0
        Q = c
    message = f"y = {A}("
    message += f"x + {P})² " if P >= 0 else f"(x - {-P})²"
    message += f"+ {Q}" if Q >= 0 else f"- {-Q}"
    return message

app  = Flask(__name__)
app.secret_key = "abcdefg"

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/vertex", methods=["POST", "GET"])
def vertex():
    form = VertexForm()
    if form.validate_on_submit():
        vertex = form.vertex.data
        point = form.point.data
        p, q = format_point(vertex)
        x, y = format_point(point)
        lowest_y = min(q,y)
        highest_y = max(q,y)
        farthest_x = (max((abs(0-p)), abs(0-x)))
        A = symbols("A")
        e = Eq(A*(x-p)**2 + q, y)
        if solve(e):
            a = solve(e, rational=True)[0]
            solution = f"y = {a}(x - {p})^2 + {q}"
            message = f"y = {a}(x{p*-1:+})² {q:+}"
            general = convert_to_general(a=a, p=p, q=q)
        else:
            message = "Those points cannot make a parabola. They are either on the same y-axis or x-axis or they are the same point."
            solution = None
            general = None
        return render_template('vertex.html', form=form, solution=solution, vertex=vertex, point=point, message=message, general=general, l_y = lowest_y, m_y = highest_y, x_b = farthest_x)
    return render_template('vertex.html', form=form)


@app.route("/three-points", methods=["POST", "GET"])
def three_points():
    form = ThreePointForm()
    if form.validate_on_submit():
        point1 = form.point_one.data
        point2 = form.point_two.data
        point3 = form.point_three.data
        solutions = solve_three(point1, point2, point3)
        solved = solutions[-1]
        message, solution = solutions[0], solutions[1]
        if solved:
            m_y, l_y, farthest_x, vertex_form = solutions[2], solutions[3], solutions[4], solutions[5]
            return render_template('three.html', form=form, message=message, solution=solution, points=[point1, point2, point3], m_y = m_y, l_y=l_y, x_b=farthest_x, solved=solved, vertex_form=vertex_form)
        else:
            return render_template('three.html', form=form, message=message, solution=solution, points=[point1, point2, point3], solved=solved)
    return render_template('three.html', form=form, points=None, solution=None)

if __name__ == "__main__":
    app.run(debug=True)

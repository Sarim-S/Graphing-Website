from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import validators, ValidationError


def valid_coordinate(form, field):
    value = field.data
    if not value.startswith("(") or not value.endswith(")"):
        raise ValidationError("Enter a valid coordinate point with bracket around it")
    try:
        x, y = value[1:-1].split(",")
    except ValueError:
        raise ValidationError("Must enter 2 points in the coordinate")
    try:
        x = x.strip()
        y = y.strip()
        float(x)
        float(y)
    except ValueError:
        raise ValidationError("Points in the coordinate must be valid numbers")
    except Exception:
        raise ValidationError("Enter a valid coordinate point")

class VertexForm(FlaskForm):
    vertex = StringField(label="Enter the vertex of the parabola",
                         validators=[validators.DataRequired(), valid_coordinate], render_kw={"autocomplete": "off"})
    point = StringField(label="Enter the point it passes through", 
                        validators=[validators.DataRequired(), valid_coordinate], render_kw={"autocomplete": "off"})
    submit = SubmitField("Calculate")

class ThreePointForm(FlaskForm):
    point_one = StringField(label="Enter the first point it passes through",
                         validators=[validators.DataRequired(), valid_coordinate], render_kw={"autocomplete": "off"})
    point_two = StringField(label="Enter the second point it passes through",
                         validators=[validators.DataRequired(), valid_coordinate], render_kw={"autocomplete": "off"})
    point_three = StringField(label="Enter the third point it passes through",
                         validators=[validators.DataRequired(), valid_coordinate], render_kw={"autocomplete": "off"})
    submit = SubmitField("Calculate")
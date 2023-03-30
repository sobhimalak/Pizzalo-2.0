from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators, DecimalField
from flask_wtf.file import FileField,FileRequired,FileAllowed

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount')
    stock = IntegerField('Stock', [validators.DataRequired()])
    colors = StringField('Allergies', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])

    image_1 = FileField('Image 1',
                        validators = [FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_2 = FileField('Image 2',
                        validators = [FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_3 = FileField('Image 3',
                        validators = [FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])


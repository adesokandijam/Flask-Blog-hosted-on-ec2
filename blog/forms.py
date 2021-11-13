from flask_wtf import FlaskForm
from sqlalchemy.orm import query
from wtforms import StringField, SubmitField, FileField, PasswordField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, ValidationError
from flask_ckeditor import CKEditorField

from blog.models import BlogPost, Portfolio


class BlogForm(FlaskForm):
    title = StringField(label="Title", validators=[DataRequired()])
    subtitle = StringField(label="Sub Heading", validators=[DataRequired()])
    body = TextAreaField(label="Post", validators=[DataRequired()])
    back_image = FileField(label = "Select the image you want added as background for post", validators=[DataRequired()])
    image = FileField(label = "Select the image you want added", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

    def validate_title(self, title_to_check):
        title = BlogPost.query.filter_by(title = title_to_check.data).first()
        if title:
            raise ValidationError('Rename or pick another image bro')
    def validate_image(self, image_to_check):
        image_name = BlogPost.query.filter_by(image_name = image_to_check.data.filename).first()
        if image_name:
            raise ValidationError('Rename or pick another image bro')

    def validate_back_image(self, back_image_to_check):
        back_image = BlogPost.query.filter_by(back_image_name = back_image_to_check.data.filename).first()
        if back_image:
            raise ValidationError('Rename or pick another image bro')



class LoginForm(FlaskForm):
    email_username = StringField(label="Enter your email or username", validators=[DataRequired()])
    password = PasswordField(label= "Enter your password", validators=[DataRequired()])
    submit = SubmitField(label = "Sign in", validators=[DataRequired()])


class PortfolioForm(FlaskForm):
    title = StringField(label='What is the name of the project?',validators=[DataRequired()])
    link = StringField(label='Kindly provide the link for the project',validators=[DataRequired()])
    github = StringField(label='Kindly provide the link to github for the project',validators=[DataRequired()] )
    submit = SubmitField(label='Submit the project')
    def validate_title(self, title):
        title = Portfolio.query.filter_by(title = title.data).first()
        if title:
            raise ValidationError('Rename the title of the Portfolio')


class CommentForm(FlaskForm):
    name = StringField(label='Name',validators=[DataRequired()])
    body = StringField(label='Comment',validators=[DataRequired()])
    submit = SubmitField(label='Submit Comment')


class EditForm(FlaskForm):
    body =CKEditorField(label="Post", validators=[DataRequired()])
    submit = SubmitField(label='Submit Comment')
    


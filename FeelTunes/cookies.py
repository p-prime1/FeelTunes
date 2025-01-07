from flask import Blueprint, render_template, request, make_response


cookies_bp = Blueprint('cookies', __name__)


@cookies_bp.route('/set_cookie/<username>')
def set_cookie(username):
    response = make_response(f"Cookie for {username} has been set!")
    response.set_cookie('username', username, max_age=60*60*24, samesite='Lax')
    return response

@cookies_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    if username:
        return f"Welcome back, {username}!"
    return "No cookie found!"

@cookies_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response("Cookie has been deleted!")
    response.set_cookie('username', '', max_age=0)
    return response

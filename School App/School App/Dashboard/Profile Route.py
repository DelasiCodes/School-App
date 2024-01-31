# dashboard.py (or a new file like profile.py)
from flask import Blueprint, render_template
from flask_login import current_user, login_required

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

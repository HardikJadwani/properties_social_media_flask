from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required


from app import db
from app.main.form import EditProfileForm, EmptyForm, PropertyForm,EditPropertyForm
from app.models import User, Property

from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    prop=None
    form = PropertyForm()
    if form.validate_on_submit():
        prop = Property(details=form.details.data,location=form.location.data,square_feet=form.square_feet.data,basement=form.basement.data,terrace=form.terrace.data,garden=form.garden.data,balcony=form.balcony.data,owner=current_user)
        db.session.add(prop)
        db.session.commit()
        flash('Your property is now added!')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    properties = current_user.followed_properties().paginate(
        page=page, per_page=current_app.config['PROPERTIES_PER_PAGE'], error_out=False)
    next_url = url_for('main.index', page=properties.next_num) \
        if properties.has_next else None
    prev_url = url_for('main.index', page=properties.prev_num) \
        if properties.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           properties=properties, next_url=next_url,
                           prev_url=prev_url)
    


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    properties = Property.query.order_by(Property.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['PROPERTIES_PER_PAGE'], error_out=False)
    next_url = url_for('main.explore', page=properties.next_num) \
        if properties.has_next else None
    prev_url = url_for('main.explore', page=properties.prev_num) \
        if properties.has_prev else None
    return render_template('index.html', title='Explore', properties=properties.items,
                           next_url=next_url, prev_url=prev_url)



@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    properties = user.properties.order_by(Property.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['PROPERTIES_PER_PAGE'], error_out=False)
    next_url = url_for('main.user', username=user.username, page=properties.next_num) \
        if properties.has_next else None
    prev_url = url_for('main.user', username=user.username, page=properties.prev_num) \
        if properties.has_prev else None
    form = EmptyForm()
    prop=Property.query.first()
    return render_template('user.html', user=user, properties=properties,next_url=next_url, prev_url=prev_url, form=form,prop=properties.items)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.contact  = form.contact.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.contact.data  = current_user.contact
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/edit_property/<int:property_id>', methods=['GET', 'POST'])
@login_required
def edit_property(property_id):
    prop=Property.query.get_or_404(property_id)
    form = EditPropertyForm()
    if form.validate_on_submit():
        prop.details = form.details.data
        prop.location = form.location.data
        prop.square_feet  = form.square_feet.data
        prop.basement  = form.basement.data
        prop.terrace  = form.terrace.data
        prop.garden  = form.garden.data
        prop.balcony  = form.balcony.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_property',property_id=property_id))
    elif request.method == 'GET':
        form.details.data=prop.details 
        form.location.data=prop.location 
        form.square_feet.data=prop.square_feet
        form.basement.data=prop.basement 
        form.terrace.data=prop.terrace
        form.garden.data=prop.garden
        form.balcony.data=prop.balcony 
    return render_template('edit_property.html', title='Edit Property',
                           form=form)





@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))



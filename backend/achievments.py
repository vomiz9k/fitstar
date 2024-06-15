from models import Achievment, UserAchievments, Image

from werkzeug import exceptions

from app import app, db

@app.route('/achievmnets/list/<int:user_id>', methods=['GET'])
def achievmentsList(user_id):
    # user_to_achievments = db.session.query(UserAchievments.user_id.label('is_locked').is_(None), Achievment.name, Achievment.description, Image.url.label('image')).join(UserAchievments, UserAchievments.achievment_id==Achievment.id, isouter=True).join(Image, Achievment.image_id==Image.id).all()
    # q = f"WITH ua AS (SELECT * FROM user_achievments WHERE user_id = {user_id}) SELECT a.name, a.description, i.url as image, ua.user_id is not null as is_unlocked FROM achievment as a LEFT JOIN image as i on a.image_id = i.id LEFT JOIN ua on ua.achievment_id = a.id"

    # achievments = db.session.execute(q)
    # result = []
    # for achievment in user_to_achievments:
    #     achievment = db.session.query(Achievment).join(Image).filter(achievment.id == achievment.id).one_or_none()
    #     if achievment is None:
    #         raise exceptions.NotFound()

    subquery = db.session.query(UserAchievments).filter(UserAchievments.user_id==user_id).subquery()
    user_to_achievments = db.session.query(Achievment.name, Achievment.description, Image.url.label('image'), subquery.c.user_id.is_not(None).label("is_unlocked")).join(subquery, subquery.c.achievment_id==Achievment.id, isouter=True).join(Image, Achievment.image_id==Image.id).all()
    return [u._asdict() for u in user_to_achievments]
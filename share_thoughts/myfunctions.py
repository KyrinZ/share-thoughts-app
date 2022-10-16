import json
from django.contrib.auth.models import User
from .models import *


# Custom function to covert post object to Json
def post_jsonify(paginated_post_object):
    post_json = [
        {
            'user_id': post_obj.user.id,
            'username': post_obj.user.username,

            'profile_pic': post_obj.user.profile.profile_pic.url,
            'nickname': post_obj.user.profile.nickname,
            'show_nickname': post_obj.user.profile.show_nickname,

            'post_id': post_obj.id,
            'date_posted': str(post_obj.date_posted.strftime("%b %d, %Y, %I:%M %p")),
            'text_field': post_obj.text_field,
            'total_likes': post_obj.likeforpost_set.count(),
            'total_comments': post_obj.comment_set.count(),

            'comments': [{
                'user_id': comment_obj.user.id,
                'username': comment_obj.user.username,

                'profile_pic': comment_obj.user.profile.profile_pic.url,
                'nickname': comment_obj.user.profile.nickname,
                'show_nickname': comment_obj.user.profile.show_nickname,

                'comment_id': comment_obj.id,
                'date_commented': str(comment_obj.date_commented.strftime("%b %d, %Y, %I:%M %p")),
                'text_field': comment_obj.text_field,
                'total_like': comment_obj.likeforcomment_set.count(),
            } for comment_obj in post_obj.comment_set.all()[:2]]
        } for post_obj in paginated_post_object]
    return json.dumps(post_json)

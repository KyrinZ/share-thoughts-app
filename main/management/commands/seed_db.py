import random
import re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Profile, Post, Comment, Follow, Hashtag
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # 1. Create Users and Profiles
        users = []
        usernames = ['alice', 'bob', 'charlie', 'diana', 'ethan', 'fiona', 'george', 'hannah', 'ian', 'julia']
        display_names = ['Alice Wonderland', 'Bob Builder', 'Charlie Brown', 'Diana Prince', 'Ethan Hunt', 
                        'Fiona Gallagher', 'George Costanza', 'Hannah Montana', 'Ian Malcolm', 'Julia Roberts']
        bios = [
            "Just a curious mind exploring the digital world.",
            "Always building something new.",
            "Living the simple life.",
            "Wondering what's next.",
            "In a mission to make the world better.",
            "Family first, always.",
            "Art and philosophy enthusiast.",
            "Dreaming big, one post at a time.",
            "Chaos theorist and nature lover.",
            "Just being myself."
        ]

        for i in range(len(usernames)):
            user, created = User.objects.get_or_create(username=usernames[i])
            if created:
                user.set_password('password123')
                user.save()
            
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.display_name = display_names[i]
            profile.bio = bios[i]
            profile.save()
            users.append(user)

        self.stdout.write(f'Successfully created {len(users)} users.')

        # 2. Create Hashtags
        tags = ['tech', 'life', 'coding', 'sharing', 'thoughts', 'design', 'future', 'mindset', 'nature', 'webdev']
        hashtag_objs = []
        for tag_name in tags:
            tag, _ = Hashtag.objects.get_or_create(name=tag_name)
            hashtag_objs.append(tag)

        # 3. Create Posts
        post_templates = [
            "Just launched my new project! #tech #coding",
            "What a beautiful day to share some #thoughts on #life.",
            "Really enjoying the new #design trends this year.",
            "Sometimes the #future seems closer than we think. #mindset",
            "Nature has a way of being simply amazing. #nature",
            "Just finished a great book on #webdev and #sharing.",
            "Working hard on something special today. #coding #tech",
            "Here's my thought for the day: stay curious. #mindset #thoughts",
            "Web development is a never-ending journey. #webdev #coding",
            "Sharing is caring! #sharing #life"
        ]

        all_posts = []
        for user in users:
            num_posts = random.randint(2, 4)
            for _ in range(num_posts):
                content = random.choice(post_templates)
                post = Post.objects.create(author=user, content=content)
                
                # Extract hashtags and link
                found_tags = re.findall(r'#(\w+)', content)
                p_tags = []
                for name in found_tags:
                    t_obj, _ = Hashtag.objects.get_or_create(name=name.lower())
                    p_tags.append(t_obj)
                post.hashtags.set(p_tags)
                all_posts.append(post)

        self.stdout.write(f'Successfully created {len(all_posts)} posts.')

        # 4. Create Comments
        comment_texts = [
            "Great work!",
            "Totally agree with this.",
            "Interesting perspective.",
            "Thanks for sharing!",
            "This is so inspiring.",
            "Could not have said it better.",
            "Keep it up!",
            "I love this!"
        ]

        comment_count = 0
        for post in all_posts:
            if random.random() > 0.3: # 70% chance of having comments
                num_comments = random.randint(1, 3)
                commenters = random.sample(users, num_comments)
                for commenter in commenters:
                    Comment.objects.create(
                        author=commenter,
                        post=post,
                        content=random.choice(comment_texts)
                    )
                    comment_count += 1

        self.stdout.write(f'Successfully created {comment_count} comments.')

        # 5. Create Follows
        follow_count = 0
        for user in users:
            others = [u for u in users if u != user]
            to_follow = random.sample(others, random.randint(2, 5))
            for target in to_follow:
                Follow.objects.get_or_create(follower=user, following=target)
                follow_count += 1

        self.stdout.write(f'Successfully created {follow_count} follow relationships.')
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))

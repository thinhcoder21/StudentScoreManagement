from django import forms
from models import Score,PostForum

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['mid_term_score', 'final_term_score']

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = PostForum
        fields = ['post_forum_title']
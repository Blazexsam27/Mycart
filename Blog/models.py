from django.db import models


class Blogpost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80, default="")
    head0 = models.CharField(max_length=100, default="")
    head0_content = models.CharField(max_length=5000, default="")
    head1 = models.CharField(max_length=100, default="")
    head1_content = models.CharField(max_length=5000, default="")
    head2 = models.CharField(max_length=100, default="")
    head2_content = models.CharField(max_length=5000, default="")
    about = models.CharField(max_length=215, default="Summary about the blog")
    pub_date = models.DateField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='shop/images', default="")

    def __str__(self):
        return self.title

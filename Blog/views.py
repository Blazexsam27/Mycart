from django.shortcuts import redirect, render
from django.http import HttpResponse
from . models import Blogpost
import random


def index(request):
    blogs = Blogpost.objects.all()
    return render(request, 'blog/index.html', {'blogs': blogs})


def blogPost(request, id):
    recommend = []
    blog = Blogpost.objects.filter(post_id=id)[0]
    allBlogs = Blogpost.objects.all()
    pblog = allBlogs[(id + 1) % Blogpost.objects.count()]
    recommend.append(pblog)
    print(allBlogs)
    return render(request, 'blog/blogPost.html', {"blog": blog, "recommend": recommend, "srange": range(0, 2)})


def createBlog(request):
    if request.method == "POST":
        title = request.POST.get('blogTitle', '')
        head0 = request.POST.get('subhead1', '')
        head0_content = request.POST.get('descHead1', '')
        head1 = request.POST.get('subhead2', '')
        head1_content = request.POST.get('descHead2', '')
        head2 = request.POST.get('subhead3', '')
        head2_content = request.POST.get('descHead3', '')
        thumbnail = request.POST.get('blogImg', '')
        about = request.POST.get('aboutBlog', '')
        blog = Blogpost(title=title, head0=head0, head0_content=head0_content, head1=head1,
                        head1_content=head1_content, head2=head2, head2_content=head2_content, thumbnail=thumbnail, about=about)

        blog.save()
        print(blog)
    return render(request, 'blog/createBlog.html')

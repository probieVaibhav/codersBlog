from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages
#import template tags
from blog.templatetags import extras
# Create your views here
# home function
def blogHome(request):
    # return HttpResponse('This is blogHome. We will keep all the blog posts here.')
    allPosts = Post.objects.all()
    return render(request, 'blog/blogHome.html', {'allPosts': allPosts})

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    repDict = {}
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno] = [reply]
        else:
            repDict[reply.parent.sno].append(reply)
    return render(request, 'blog/blogPost.html', {'post': post, 'comments': comments, 'user': request.user, 'repDict': repDict})
    # return HttpResponse(f'This is blogPost: {slug}')

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment') 
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')

        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, 'your comment has been posted successfully')
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, 'your reply has been posted successfully')
        '''if len(comment) >= 10:
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, 'your comment has been posted successfully')
        else:
            messages.error(request, 'Comment must be of more than 10 characters')'''
    else:
        return HttpResponse('404 - not found')

    return redirect(f'/blog/{post.slug}')
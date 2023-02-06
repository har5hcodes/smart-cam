from django import template
from displaycode.models import Snippet, Comment

register = template.Library()

#https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/

#Filter which takes a codeLine and its Id. spits out 
@register.filter
def displayCommentsFilter(snippetId, line):

    allComments = Comment.objects.filter(line=line).filter(snippetId=snippetId)
    result = ""
    for comment in allComments:
        x = comment.text
        result = result + x
        #print (x)
    return result
    #"raghuram"+str(lineNum)



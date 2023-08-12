from .models import FriendRequest
from django.db.models import Q
def friendRequests(request):
    
    f_requests = FriendRequest.objects.filter(to = request.user.id, status = "unchecked").select_related('sender')
    my_friends = FriendRequest.objects.filter(Q(to = request.user.id) & Q(status = "accepted")) | FriendRequest.objects.filter(Q(sender = request.user.id) & Q(status = "accepted"))
    print(my_friends)
    return {'friends_requests':f_requests, 'friends':my_friends}


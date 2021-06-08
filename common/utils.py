import hashlib


def get_finger_print(request):
    h = hashlib.sha256()
    h.update(bytes(request.META.get('HTTP_USER_AGENT', ''), encoding='utf8'))
    h.update(bytes(request.META.get('REMOTE_ADDR', ''), encoding='utf8'))
    if (request.user.id):
        h.update(bytes(request.user.id))
    return h.hexdigest()

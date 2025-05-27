from . import models

def basket_middleware(get_response):
    def middleware(request):
        basket = None
        basket_id = request.session.get('basket_id')
        if basket_id:
            try:
                basket = models.Basket.objects.get(id=basket_id)
            except models.Basket.DoesNotExist:
                basket = None
        request.basket = basket
        response = get_response(request)
        return response
    return middleware
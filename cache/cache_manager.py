import hashlib
from redis import Redis

class CacheManager:
    def __init__(self):
        self.redis = Redis(host='localhost', port=6379, db=0)

    def is_price_changed(self, product):
        product_hash = hashlib.md5(f"{product['product_title']}_{product['current_price']}".encode()).hexdigest()
        cached_hash = self.redis.get(product['product_title'])

        if cached_hash == product_hash:
            return False

        self.redis.set(product['product_title'], product_hash)
        return True

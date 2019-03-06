import orm
import asyncio
from models import User, Blog, Comment

async def insert(loop):
    await orm.create_pool(loop=loop, host='192.168.1.131', user='root', password='365598966', db='awesome')
    u = User(name='Test', email='test@example.com', passwd='123456', image='about:blank')
    await u.save()
    await orm.destory_pool()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(insert(loop))
    loop.close()
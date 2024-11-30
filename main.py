import redis
from redis.exceptions import RedisError


def main():
    try:
        pool = redis.ConnectionPool(host='192.168.0.207', port=6379, decode_responses=True)
        redis_client = redis.Redis(connection_pool=pool)

        print("Pinging Redis server...")
        if redis_client.ping():
            print("Connected to Redis successfully!")

        print("\n--- Strings ---")
        redis_client.set('username', 'german_gerken')
        print(f"Username: {redis_client.get('username')}")

        print("\n--- Hashes ---")
        redis_client.hset('user:1', mapping={
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'age': '30'
        })
        user = redis_client.hgetall('user:1')
        print(f"User details: {user}")

        print("\n--- Lists ---")
        redis_client.rpush('tasks', 'task1', 'task2', 'task3')
        tasks = redis_client.lrange('tasks', 0, -1)
        print(f"Tasks: {tasks}")

        print("\n--- Sets ---")
        redis_client.sadd('unique_visitors', 'visitor1', 'visitor2', 'visitor3', 'visitor1')  # Duplicate ignored
        visitors = redis_client.smembers('unique_visitors')
        print(f"Unique visitors: {visitors}")

        print("\n--- Sorted Sets ---")
        redis_client.zadd('leaderboard', {'Alice': 150, 'Bob': 120, 'Charlie': 180})
        leaderboard = redis_client.zrange('leaderboard', 0, -1, withscores=True)
        print(f"Leaderboard: {leaderboard}")

        print("\n--- Expiring Keys ---")
        redis_client.set('temp_key', 'This will expire', ex=10)
        print(f"Temp key: {redis_client.get('temp_key')}")
        print("Waiting for 10 seconds...")
        import time
        time.sleep(10)
        print(f"Temp key after expiration: {redis_client.get('temp_key')}")

    except RedisError as e:
        print(f"Redis error: {e}")
    except Exception as e:
        print(f"General error: {e}")
    finally:
        if pool:
            pool.disconnect()


if __name__ == "__main__":
    main()
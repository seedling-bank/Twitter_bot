import tracemalloc

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
import pytz

from hub.automatically_mbti_bot import automatically_mbti
from hub.automatically_reply_bot import automatically_reply
from hub.automatically_tweet_bot import automatically_tweet

jobstores = {
    # 'default': MongoDBJobStore(collection='apschedule_job', database=CONF['MONGODB_CONFIG']['DB'], client=client)
    "default": MemoryJobStore()
}

executors = {"default": ThreadPoolExecutor(20), "processpool": ProcessPoolExecutor(3)}

job_defaults = {"coalesce": False, "max_instances": 5}

scheduler = BlockingScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone=pytz.timezone("asia/Shanghai"),
)

tracemalloc.start()

scheduler.add_job(automatically_tweet.run, **automatically_tweet.get_scheduler())
scheduler.add_job(automatically_reply.run, **automatically_reply.get_scheduler())
scheduler.add_job(automatically_mbti.run, **automatically_mbti.get_scheduler())
scheduler.start()

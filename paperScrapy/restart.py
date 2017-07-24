import os, time, sched
import multiprocessing

schedule = sched.scheduler(time.time, time.sleep)

cmd = '''
kill -9 `ps -aux|grep 'python run.py'|awk '{print $2}'`
'''
cmd2 = 'python run.py '


def start_test(c2):
    os.system(c2)
    print time.ctime(), 'scrapy is running'


def recycle_eval(c1, c2, inc):

    schedule.enter(inc, 0, recycle_eval, (c1, c2, inc))
    os.system(c1)
    print time.ctime(), 'scrapy is killed'
    p = multiprocessing.Process(target=start_test, args=(c2 + '0',))
    p.start()


if __name__ == '__main__':

    # p = multiprocessing.Process(target=start_test, args=(cmd2 + '0',))
    # p.start()
    #
    # inc = 600
    # schedule.enter(inc, 0, recycle_eval, (cmd, cmd2, inc))
    # schedule.run()

    os.system(cmd2)
    print time.ctime(), 'scrapy is running'
    while True:
        # time.sleep(10)
        os.system(cmd)
        print time.ctime(), 'scrapy is killed'
        os.system(cmd2)
        print time.ctime(), 'scrapy is running'


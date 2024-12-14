import random
import traceback

import loguru


def get_search_term(search_list):
    """
    随机获取一个搜索词
    :param search_list:
    :return:
    """
    try:
        search = random.choice(search_list)
        return search
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())


def main():
    try:
        search_list = ['btc', 'eth', 'web3', 'ai', 'agent']
        result = get_search_term(search_list)
        print(result)
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())


if __name__ == '__main__':
    main()

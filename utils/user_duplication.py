import traceback

import loguru

user_list = list()


def verify_user_duplication(user_id):
    """
    验证是否已经使用过user
    :return:
    """
    try:
        if user_id in user_list:
            return False
        else:
            user_list.append(user_id)
            return True
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())

# -*- coding: utf-8 -*-
import os
import shutil
import locale


class Path(object):
    # 初始地址,不含分隔符
    # 此时sys.stdout.encoding已被修改为utf-8，故改为使用locale.getpreferredencoding()获取默认编码
    base_path = unicode(os.path.abspath('.').decode(locale.getpreferredencoding()))

    config_path = base_path + u'/config.json'
    db_path = base_path + u'/zhihuDB_173_1.db'
    sql_path = base_path + u'/db/zhihuhelp.sql'

    www_css = base_path + u'/www/css'
    www_image = base_path + u'/www/images'

    html_pool_path = base_path + u'/知乎电子书临时资源库/知乎网页池'
    image_pool_path = base_path + u'/知乎电子书临时资源库/知乎图片池'
    result_path = base_path + u'/知乎助手生成的电子书'
    answer_path = base_path + u'./答案'

    @staticmethod
    def reset_path():
        Path.chdir(Path.base_path)
        return

    @staticmethod
    def pwd():
        print os.path.realpath('.')
        return

    @staticmethod
    def get_pwd():
        path = unicode(os.path.abspath('.').decode(locale.getpreferredencoding()))
        return path

    @staticmethod
    def mkdir(path):
        try:
            os.mkdir(path)
        except OSError:
            # Debug.logger.debug(u'指定目录已存在')
            pass
        return
        
    @staticmethod
    def mkdirs(path):
        try:
            os.makedirs(path)
        except Exception:
            return False
        return True

    @staticmethod
    def chdir(path):
        try:
            os.chdir(path)
        except Exception as e:
            # Debug.logger.debug(u'指定目录不存在，自动创建之')
            print e
            Path.mkdir(path)
            os.chdir(path)
            
        return

    @staticmethod
    def rmdir(path):
        if path:
            shutil.rmtree(path, ignore_errors=True)
        return

    @staticmethod
    def copy(src, dst):
        if not os.path.exists(src):
            # Debug.logger.info('{}不存在，自动跳过'.format(src))
            return
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy(src=src, dst=dst)
        return

    @staticmethod
    def get_filename(src):
        return os.path.basename(src)

    @staticmethod
    def init_base_path():
        Path.base_path = Path.get_pwd()

        Path.config_path = Path.base_path + u'/config.json'
        Path.db_path = Path.base_path + u'/zhihuDB_173_1.db'
        Path.sql_path = Path.base_path + u'/db/zhihuhelp.sql'

        Path.www_css = Path.base_path + u'/www/css'
        Path.www_image = Path.base_path + u'/www/images'

        Path.html_pool_path = Path.base_path + u'/知乎电子书临时资源库/知乎网页池'
        Path.image_pool_path = Path.base_path + u'/知乎电子书临时资源库/知乎图片池'
        Path.result_path = Path.base_path + u'/知乎助手生成的电子书'
        Path.answer_path = Path.base_path + u'./答案'

        return

    @staticmethod
    def init_work_directory():
        Path.reset_path()
        Path.mkdir(u'./知乎助手生成的电子书')
        Path.mkdir(u'./知乎电子书临时资源库')
        Path.chdir(u'./知乎电子书临时资源库')
        Path.mkdir(u'./知乎网页池')
        Path.mkdir(u'./知乎图片池')
        Path.mkdir(u'./答案')
        Path.reset_path()
        return

    @staticmethod
    def is_file(path):
        return os.path.isfile(path)
    @staticmethod
    def is_dir(path):
        return os.path.isdir(path)
    @staticmethod
    def join_dir(path,filename):
        return os.path.join(path,filename)

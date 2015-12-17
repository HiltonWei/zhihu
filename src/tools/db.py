# -*- coding: utf-8 -*-
from debug import Debug
from src.tools.type import Type
import pdb
from src.tools.path import Path
import hashlib

class DB(object):
    u'''
    用于存放常用的sql代码
    '''
    cursor = None
    conn = None

    @staticmethod
    def set_conn(conn):
        DB.conn = conn
        DB.conn.text_factory = str
        DB.cursor = conn.cursor()
        return

    @staticmethod
    def execute(sql):
        return DB.cursor.execute(sql)

    @staticmethod
    def commit():
        return DB.cursor.commit()

    @staticmethod
    def save(data={}, table_name=''):
        if table_name == 'Answer':
            DB.addFileSave(data)
        sql = "replace into {table_name} ({columns}) values ({items})".format(table_name=table_name,
                                                                              columns=','.join(data.keys()),
                                                                              items=(',?' * len(data.keys()))[1:])
        # BaseClass.logger.debug(sql)
        if not data:#空数据
            return
        DB.cursor.execute(sql, tuple(data.values()))
        return

    @staticmethod
    def commit():
        DB.conn.commit()
        return

    @staticmethod
    def get_result_list(sql):
        Debug.logger.debug(sql)
        result = DB.cursor.execute(sql).fetchall()
        return result

    @staticmethod
    def get_result(sql):
        result = DB.cursor.execute(sql).fetchone()
        return result

    @staticmethod
    def wrap(kind, result=()):
        u"""
        将s筛选出的列表按SQL名组装为字典对象
        """
        template = {Type.answer: (
            'author_id', 'author_sign', 'author_logo', 'author_name', 'agree', 'content', 'question_id', 'answer_id',
            'commit_date', 'edit_date', 'comment', 'no_record_flag', 'href',),
            Type.question: ('question_id', 'comment', 'views', 'answers', 'followers', 'title', 'description',),
            Type.article: ('author_id', 'author_hash', 'author_sign', 'author_name', 'author_logo', 'column_id', 'name',
                           'article_id', 'href', 'title', 'title_image', 'content', 'comment', 'agree',
                           'publish_date',),

            Type.author_info: (
                'logo', 'author_id', 'hash', 'sign', 'description', 'name', 'asks', 'answers', 'posts', 'collections',
                'logs', 'agree', 'thanks', 'collected', 'shared', 'followee', 'follower', 'followed_column',
                'followed_topic', 'viewed', 'gender', 'weibo',),
            Type.collection_info: ('collection_id', 'title', 'description', 'follower', 'comment',),
            Type.topic_info: ('title', 'logo', 'description', 'topic_id', 'follower',), Type.column_info: (
                'creator_id', 'creator_hash', 'creator_sign', 'creator_name', 'creator_logo', 'column_id', 'name',
                'logo', 'description', 'article', 'follower',),

            Type.collection_index: ('collection_id', 'href',), Type.topic_index: ('topic_id', 'href',), }
        return {k: v for (k, v) in zip(template[kind], result)}
    @staticmethod
    def addFileSave(answertmp={}):
        save_content = hashlib.md5(answertmp['content']).hexdigest()
        def dodir(answertmp = []):
            if answertmp:
                answerpath = Path.answer_path+'/Answer_qid_aid/'+answertmp['question_id'] 
                if not Path.is_dir(answerpath):
                    Path.mkdirs(answerpath)
                filename = answertmp['question_id']+'_'+answertmp['answer_id']+'.txt'
            return Path.join_dir(answerpath,filename)
        filepath_name = dodir(answertmp)
        def isUpdateContent( save_content ,questionID , answerID):#是否更答案文本内容
            answerHref = 'http://www.zhihu.com/question/{0}/answer/{1}'.format(questionID, answerID)
            Var = DB.cursor.execute(
                    "select content from Answer  where href = ?", (answerHref,)).fetchone()
            if not Var:
                Debug.logger.debug(u'读答案md5失败')
                return False #初始为空 则默认插入
            return Var[0] == save_content
        bsaved = isUpdateContent(save_content , answertmp['question_id'] , answertmp['answer_id'])
        if not Path.is_file(filepath_name):
            bsaved = False#数据库中有，文件没有
        if not bsaved :
            DB.svContent2File(filepath_name , answertmp['content'])
        answertmp['content'] = str(save_content)
        return
    @staticmethod
    def svContent2File( filepath_name , contentInHttp):
        contentBefore=''
        if Path.is_file(filepath_name):
            with open(filepath_name , 'r' ) as f:
                contentBefore = f.read()
        def calcContent(contentBefore ,contentSave):#计算内容 是否保存
            strContentSave = contentSave
            if (contentSave.find(contentBefore[10:]) == -1):
                strContentSave += '\n -----------------------------------------答案更新分割线------------------\n'
                strContentSave += contentBefore
            return strContentSave
        content2SV = calcContent(contentBefore , contentInHttp)
        with open(filepath_name ,'w') as f:
            f.write(content2SV)
        return

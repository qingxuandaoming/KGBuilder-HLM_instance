from py2neo import Graph

# Default configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "950302" # Default password, override in local_config.py

# Try to import local configuration
try:
    from neo_db.local_config import NEO4J_URI as LOCAL_URI, NEO4J_USER as LOCAL_USER, NEO4J_PASSWORD as LOCAL_PASSWORD
    NEO4J_URI = LOCAL_URI
    NEO4J_USER = LOCAL_USER
    NEO4J_PASSWORD = LOCAL_PASSWORD
except ImportError:
    pass

graph = Graph(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

CA_LIST = {"贾家荣国府":0,"贾家宁国府":1,"王家":2,"史家":3,"薛家":4,"其他":5,"林家":6}
similar_words = {
    "爸爸": "父亲",
    "妈妈": "母亲",
    "爸": "父亲",
    "妈": "母亲",
    "父亲": "父亲",
    "母亲": "母亲",
    "儿子":"儿子",
    "女儿":"女儿",
    "丫环":"丫环",
    "丫鬟":"丫环",
    "丫头":"丫头",
    "兄弟":"兄弟",
    "妻":"妻",
    "妻子":"妻",
    "夫人":"妻",
    "老婆":"妻",
    "哥哥":"哥哥",
    "表妹":"表兄妹",
    "表姐":"表兄妹",
    "弟弟":"弟弟",
    "妾":"妾",
    "养父":"养父",
    "姐姐":"姐姐",
    "娘":"母亲",
    "爹":"父亲",
    "father":"父亲",
    "mother":"母亲",
    "朋友":"朋友",
    "爷爷":"爷爷",
    "奶奶":"奶奶",
    "祖父":"爷爷",
    "祖母":"奶奶",
    "孙子":"孙子",
    "老公":"丈夫",
    "夫君":"丈夫",
    "丈夫":"丈夫",
    '岳母': '岳母',
    '岳父': '岳父',
    "表兄妹":"表兄妹",
    "孙女": "孙女",
    "嫂子":"嫂子",
    "暧昧":"暧昧",
    "老师": "老师",
    "朋友": "朋友",
    "好朋友": "朋友",
    "好友": "朋友",
    "好兄弟": "兄弟",
    "夫妻": "夫妻",
    "伯父": "伯父",
    "姑母": "姑母",
    "侄女": "侄女",
    "侄儿": "侄儿",
    "外祖父": "外祖父",
    "外祖母": "外祖母",
    "外公": "外祖父",
    "外婆": "外祖母",
    "外孙女": "外孙女",
    "乳母": "乳母",
    "乾娘": "乾娘",
    "小厮": "小厮",
    "相好": "相好",
    "陪房": "陪房",
    "陪房丫头": "陪房丫头",
    "被抚养": "被抚养",
    "内侄女": "内侄女",
    "父": "父亲",
    "母": "母亲",
}

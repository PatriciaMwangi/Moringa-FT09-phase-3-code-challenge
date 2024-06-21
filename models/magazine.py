import sqlite3
conn =sqlite3.Connection("magazine.db")
cursor=conn.cursor()
from article import Article
from collections import Counter

class Magazine:
    all={}
    def __init__(self, id, name, category=None):
        self._id=None
        self.id = id
        self._name=None
        self._category=category
        self.name = name
        
        type(self).all[self.id]=self

    def __repr__(self):
        return f'<Magazine {self.name}>'
    
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self,id):
        if not isinstance(id,int):
             raise ValueError("Must be of type integer")
        self._id=id 

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,name):
        if not isinstance(name,str) or not (2 <= len(name) <= 16):
            raise ValueError("Must be a string between 2 and 16 characters")
        self._name=name

    @property
    def category(self):
        return self._category    
    @category.setter
    def category(self,category):
        if not isinstance(category,str) or len(category) == 0:
            raise ValueError("Must be a non empty str")
        self._category=category

    @classmethod
    def create_table(cls):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS magazine(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT)
            """)
        conn.commit()

    @classmethod
    def drop_table(cls):
        cursor.execute('DROP TABLE IF EXISTS magazine')
        conn.commit()
    
    def save(self):
        cursor.execute("""INSERT INTO magazine(id,name,category) VALUES(?,?,?)""",(self.id,self.name,self.category))
        conn.commit()
        type(self).all[self.id]=self

    @classmethod
    def create(cls,id,name,category):
        magazine=cls(id,name,category)
        magazine.save()
        return magazine
    
    def articles(self):
        from article import Article
        cursor.execute("""
        SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
        FROM articles
        WHERE articles.magazine_id = ?
        """, (self.id,))
    
        rows = cursor.fetchall()
        articles = []
        for row in rows:
            article_id, article_title, article_content, author_id, magazine_id = row
        # Ensure all required attributes are passed to Article constructor
            article = Article(id=article_id, title=article_title, content=article_content, author_id=author_id, magazine_id=magazine_id)
            articles.append(article)
    
        return articles if articles else None
        
    def contributors(self):
        from author import Author
        cursor.execute("""SELECT authors.id,authors.name
                       FROM magazines JOIN authors
                       ON magazine.id = authors.id
                       WHERE magazines.id =?
                       """,(self.id))
        row=cursor.fetchone()
        if row:
            authors_id,authors_name=row
            return Author(authors_id,authors_name)
        else:
            return None
        
    def article_titles(self):
        titles= [article.title for article in Article.all.values() if article.magazine_id== self.id]
        return titles if titles else None
    def contributing_authors(self):
        authors=Counter(article.author_id for article in Article.all.values() if article.magazine_id== self.id)
        authors_count=[author for author,count in authors.items() if count > 2 ]
        return authors_count if authors_count else None

Magazine.drop_table()
Magazine.create_table()
Magazine.create(id=1,name="Vogue Fashion",category="Fashion")
mag=Magazine(id=1,name="Vogue Fashion",category="Fashion")

m=mag.articles()
print(m)
 
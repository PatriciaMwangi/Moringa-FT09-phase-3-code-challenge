import sqlite3
conn =sqlite3.Connection("magazine.db")
cursor=conn.cursor()

class Article:
    all={}

    def __init__(self, title, content, author_id, magazine_id, id=None):
        self._title=None
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        if id is None:
            self.id= max(self.all.keys(),default=0)+1
        else:
            self.id =id

        type(self).all[self.id]=self
        print (f'articles added: {self}')


    def __repr__(self):
        return f'<Article {self.title}: {self.author_id}>'

    @property
    def title(self):
        return self._title
    @title.setter
    def title(self,title):
        print(f"Setting title: {title}")  # Debug statement
        if not isinstance(title, str):
            print("Title is not a string")  # Debug statement
            raise ValueError("Must be type string between 5 and 50 characters")
        if not (5 <= len(title) <= 50):
            print(f"Title length is {len(title)}")  # Debug statement
            raise ValueError("Must be type string between 5 and 50 characters")
        if self._title is not None:
            print("Title has already been set")  # Debug statement
            raise ValueError("Seems like the title has been set already")
        self._title = title

    
    @classmethod
    def create_table(cls):
        sql="""
        CREATE TABLE IF NOT EXISTS articles(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TETX NOT NULL,
        author_id INTEGER NOT NULL,
        magazine_id INTEGER NOT NULL,
        FOREIGN KEY (author_id) REFERENCES authors(id),
        FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        )
        """
        cursor.execute(sql)
        conn.commit()

    @classmethod
    def drop_table(cls):
        cursor.execute('DROP TABLE IF EXISTS magazine')
        conn.commit()

    @classmethod
    def create_row(cls,title,content,author_id,magazine_id):
        cursor.execute("""SELECT * FROM articles WHERE title=? AND content=? AND author_id=? AND magazine_id=?""",
                       (title,content,author_id,magazine_id))
        repeated=cursor.fetchone()
        if repeated:
            print("All the values provided have been recorded before")
            return None
        else:
            sql="""
            INSERT INTO articles(title,content,author_id,magazine_id) VALUES(?,?,?,?)
            """
            cursor.execute(sql,(title,content,author_id,magazine_id))
            conn.commit()
            article_id=cursor.lastrowid
            Article.all[article_id]=repeated

            article=cls(title,content,author_id,magazine_id,article_id)
            return article
    
    @classmethod
    def instance_from_db(cls,row):
        article=cls(
            title=row['title'],
            content=row['content'],
            author_id=row['author_id'],
            magazine_id=row['magazine_id']

        )
        cls.all[article.id]=article
        return article
    
    def delete(self):
        cursor.execute("""DELETE FROM articles WHERE id =?""",(self.id,))
        conn.commit()
        del type(self).all[self.id]
        self.id=None

    def author(self):
        from author import Author
        cursor.execute("""
        SELECT authors.id,authors.name
        FROM articles
        JOIN authors ON articles.author_id=authors.id
        WHERE authors.id = ?
        """, (self.id,))
        row =cursor.fetchone()
        if row:
            author_id,author_name=row
            return Author(author_id,author_name)
        else:
            return None
        
    def magazine(self):
        from magazine import Magazine
        cursor.execute("""
        SELECT magazines.id,magazines.name
        FROM articles
        JOIN magazines ON articles.magazine_id=magazines.id
        WHERE magazines.id=?""",(self.id,))
        row= cursor.fetchone()
        if row:
            magazines_id,magazines_name=row
            return Magazine(magazines_id,magazines_name)  
        else:
            return None      
        
#print(Article.all)
Article.drop_table
Article.create_table()
articles=Article.create_row(title="Tech Weekly",content= "Today's World",author_id= 1,magazine_id=2)
article={'id':9,'title':"Tech Weekly",'content': "Technology",'author_id': 1,'magazine_id':2}
article1 = Article(id=1, title="Tech Trends", content="Latest in tech", author_id=1, magazine_id=1)
article2 = Article(id=2, title="AI Innovations", content="AI news", author_id=1, magazine_id=1)
article3 = Article(id=3, title="Health Tips", content="Tips for healthy living", author_id=1, magazine_id=1)

#print(Article.all)
Article.instance_from_db(article) 
print(Article.all)

#articles.delete()




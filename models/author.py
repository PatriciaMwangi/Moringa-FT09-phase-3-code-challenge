import sqlite3
conn =sqlite3.Connection("magazine.db")
cursor=conn.cursor()


class Author:
    all={}
    def __init__(self,id,name):
        self._id=None
        self.id = id
        self._name=None
        self.name = name
        
        type(self).all[self.id]=self

    def __repr__(self):
        return f'<Author {self.name}>'
    
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self,id):
        if not isinstance(id,int):
            raise ValueError("Must be an integer")
        self._id=id
    
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,name):
        if not isinstance(name,str) or len(name)== 0:
            raise ValueError("Must be a non empty string")
        if self._name is not None:
            raise ValueError("Sorry thne name has been set already")
        self._name=name

    @classmethod
    def create_table(cls):
        
        sql="""
                CREATE TABLE IF NOT EXISTS authors(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
                )
                """
        cursor.execute(sql)
        conn.commit()

    def save(self):
        cursor.execute("""INSERT INTO authors(id,name) VALUES(?,?)""",(self.id,self.name))
        conn.commit()
        self.id=cursor.lastrowid
        type(self).all[self.id]=self

    @classmethod
    def create_row(cls,id,name):
        author=cls(id,name)
        author.save()
        return author
    
    def delete(self):
        cursor.execute('DELETE FROM authors WHERE id = ?',(self.id,))
        conn.commit()
        del type(self).all[self.id]
        
    
    def articles(self):
        from .article import Article
        cursor.execute("""
        SELECT articles.id,articles.title,articles.content,articles.author_id,articles.magazine_id
        FROM articles
        JOIN authors ON authors.id=articles.author_id WHERE authors.id =?
        """,(self.id,))
        rows = cursor.fetchall()
        articles=[]
        #print(f"Fetched rows for author {self.id}: {row}")  # Debugging line

        for row in rows:
            article_id, article_title, article_content, author_id, magazine_id = row
            article = Article(id=article_id, title=article_title, content=article_content,
                              author_id=author_id, magazine_id=magazine_id)
            articles.append(article)
        
        return articles if articles else None
    
    def magazines(self):
        from magazine import Magazine
        cursor.execute("""
            SELECT magazines.id,magazines.name
        FROM authors JOIN magazines ON authors.id=magazines.id""",(self.id,))
        row=cursor.fetchall()
        if row:
            return[Magazine(magazine_name) for magazine_name in row]
        else:
            return None

Author.create_table()        
author=Author(id=1,name="Patricia Mwangi")
author.articles()


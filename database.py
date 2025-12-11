import sqlite3
from schema import ShipmentUpdate , ShipmentCreate
from typing import Any
import sqlite3
from contextlib import contextmanager

class Database:
    def connect_to_db(self):
        # Make Connection with database 
        self.conn = sqlite3.connect("./sqlite.db"  ,check_same_thread=False)
        # Get cursor to databse 
        self.cur = self.conn.cursor()
        # create table if not created 
        self.create_table()
        print("connection to the database")
        
    def create_table(self ):
        # 1. Create table if not exists
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS shipment (
                Id  INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                status TEXT
            )
        """ )
    
    def create(self , shipment:ShipmentCreate) -> int:
        # find new id 
        self.cur.execute(""" 
            SELECT MAX(id) FROM shipment
        """)
        result  = self.cur.fetchone()
        
        new_id = result[0] + 1
        # insert into  database 
        
        self.cur.execute("""
            INSERT INTO shipment 
            VALUES (:id , :content, :weight , :status)
        """ , 
            {
                "id": new_id,
                **shipment.model_dump(),
                "status": "placed"
            }
        )
        # commit changes 
        self.conn.commit()
        
        return new_id
    
    def get(self , id:int) -> dict[str , Any] | None:
        self.cur.execute("""
            SELECT * from shipment
            WHERE id = ?
        """ , (id, ))
        
        row = self.cur.fetchone()
        
        return { 
            "id": row[0],
            "content": row[1],
            "weight": row[2],
            "status": row[3]
        } if row else None 
    
    def update(self , id:int , shipment: ShipmentUpdate) -> dict[str , Any]:
        # update shipment 
        self.cur.execute("""
            UPDATE shipment SET status = :status
            WHERE id = :id
        """,
            {
                "id": id,
                **shipment.model_dump()
            }
        )
        self.conn.commit()
        
        return self.get(id)
    
    def delete(self , id :int):
        self.cur.execute("""
            DELETE FROM shipment
            WHERE  Id = ?
        """ , (id, ))
        self.conn.commit()
        
    def close(self):
        print(".... connection is being closed ")
        self.conn.close()
    
    def __enter__(self):
        print("entering context")
        self.connect_to_db()
        self.create_table()
        return self


    def __exit__(self , *args):
        print("exit context")
        self.close()
        
    
# usage 
@contextmanager
def manage_db():
    
    db = Database()
    print("connection to database")
    # setup 
    db.connect_to_db()
    db.create_table()
    
    yield db
    
    print("exit context ")
    # close connection 
    db.close()


with manage_db() as db: 
    print(db.get(12701))
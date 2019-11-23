from app import *
import models

if __name__ == "__main__":
    db.create_all()
    manager.run()


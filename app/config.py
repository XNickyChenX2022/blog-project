class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://{username}:{password}@{host}/{database_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
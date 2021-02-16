from helpers.mongoConnection import *
from helpers.checking import *
from bson import ObjectId
from helpers.settings import *

def setup(typ):
    if typ == "movies":
        return movies_set
    elif typ == "celebrities":
        return celebrities_set

def insert(obj,typ):
    settings = setup(typ)

    if not check_params(obj,settings['obligatory']):
        return {"response":400, "message": f"Bad Request: {settings['obligatory']} are obligatory parameters"}

    q = {settings['name']:obj[settings['name']]}

    if check_exists(q,typ):
        return {"response":400,"message": f"Bad Request: there is already a {settings['sing']} with that name"}

    res = write_coll(typ,obj)
    return res.inserted_id

def list_all(typ):
    settings = setup(typ)

    res = read_coll(typ,{})
    response = {c[settings['name']]:str(c['_id']) for c in res}
    
    return response 

def get(obj,typ):
    settings = setup(typ)

    if not check_params(obj,['id']):
        return {"response":400,"message":"Bad Request: 'id' is an obligatory parameter"}

    q = {"_id":ObjectId(obj['id'])}
    if not check_exists(q,typ):
        return {"response":400,"message": f"Bad Request: {settings['sing']} with given id does not exist"}
    
    return read_coll(typ,q)

def delete(obj,typ):
    settings = setup(typ)

    if not check_params(obj,['id']):
        return {"response":400,"message":"Bad Request: 'id' is an obligatory parameter"}

    q = {"_id":ObjectId(obj['id'])}
    if not check_exists(q,typ):
        return {"response":400,"message": f"Bad Request: {settings['sing']} with given id does not exist"}

    delete_coll(typ,q)
    return {"response":200,"message": f"{settings['sing']}  successfully deleted"}

def update(obj,typ):
    settings = setup(typ)

    if not check_params(obj,['id'],settings['at_least_one']):
        return {"response":400,"message": f"Bad Request: 'id' and at least one of {settings['at_least_one']} are obligatory parameters"}
    
    q = {"_id":ObjectId(obj['id'])}
    if not check_exists(q,typ):
        return {"response":400,"message": f"Bad Request: {settings['sing']} with given id does not exist"}
    
    obj.pop("id")
    update_coll(typ,q,obj)
    return {"response":200, "message": f"{settings['sing']} successfully updated"}

def add_cast(obj):
    if not check_params(obj,['movie_id','celebrity_id']):
        return {"response":400,"message":"Bad Request: 'movie_id' and 'celebrity_id' are obligatory parameters"}
    movie = {"_id":ObjectId(obj['movie_id'])}
    
    if not check_exists(movie,"movies"):
        return {"response":400,"message":"Bad Request: movie with given id does not exist"}
    celebrity = {"_id":ObjectId(obj['celebrity_id'])}
    
    if not check_exists(celebrity,"celebrities"):
        return {"response":400,"message":"Bad Request: celebrity with given id does not exist"}
    
    push_coll("movies",movie,{"cast":celebrity['_id']})
    return {"response":200,"message":"movie cast successfully updated"}

def get_works(obj):
    if not check_params(obj,['id']):
        return {"response":400,"message":"Bad Request: 'id' is an obligatory parameter"}

    q = {"_id":ObjectId(obj['id'])}
    if not check_exists(q,"celebrities"):
        return {"response":400,"message":"Bad Request: celebrity with given id does not exist"}

    cel = list(read_coll("celebrities",q))[0]
    query = {"cast":q['_id']}
    res = read_coll("movies",query)
    return {"name":cel['name'],"works":[movie['title'] for movie in res]}

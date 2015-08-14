import json

from flask import request, Response, url_for, render_template # need render_template for abort method
from jsonschema import validate, ValidationError

import models
import decorators
from posts import app
from database import session

def post_not_found(id):
    message = "Could not find post with id {}".format(id)
    data = json.dumps({"message": message})
    return Response(data, 404, mimetype="application/json")

@app.route("/api/posts/<int:id>", methods=["GET"])
@decorators.accept("application/json")
def post_get(id):
    """ Single post endpoint """
    # Get the post from the database
    post = session.query(models.Post).get(id)

    # Check whether the post exists
    # If not return a 404 with a helpful message
    if not post:
        return post_not_found(id)

    # Return the post as JSON
    data = json.dumps(post.as_dictionary())
    return Response(data, 200, mimetype="application/json")

    
# @app.route("/api/posts", methods=["GET"])  ### superseded code
# @decorators.accept("application/json")
# def posts_get():
#     """ Get a list of posts """

#     # Get the posts from the database
#     posts = session.query(models.Post).order_by(models.Post.id)

#     # Convert the posts to JSON and return a response
#     data = json.dumps([post.as_dictionary() for post in posts])
#     return Response(data, 200, mimetype="application/json")
    
@app.route("/api/posts", methods=["GET"])
@decorators.accept("application/json")
def posts_get():
    """ Get a list of posts """
    # Get the querystring arguments
    title_like = request.args.get("title_like")
    body_like = request.args.get("body_like")
   
    # Get and filter the posts from the database
    posts = session.query(models.Post)
    if title_like and body_like:
        posts = posts.filter(models.Post.title.contains(title_like))
        posts = posts.filter(models.Post.body.contains(body_like))
    elif title_like:
        posts = posts.filter(models.Post.title.contains(title_like))
    elif body_like:
        posts = posts.filter(models.Post.body.contains(body_like))
        
        
    posts = posts.order_by(models.Post.id)

    # Convert the posts to JSON and return a response
    data = json.dumps([post.as_dictionary() for post in posts])
    return Response(data, 200, mimetype="application/json")
    
    
@app.route("/api/posts", methods=["POST"])
@decorators.accept("application/json")
def posts_post():
    """ Add a new post """
    data = request.json

    # Add the post to the database
    post = models.Post(title=data["title"], body=data["body"])
    session.add(post)
    session.commit()

    # Return a 201 Created, containing the post as JSON and with the
    # Location header set to the location of the post
    data = json.dumps(post.as_dictionary())
    headers = {"Location": url_for("post_get", id=post.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")
    

@app.route("/api/posts/<int:id>", methods =["DELETE"])
def post_delete(id):
    post = session.query(models.Post).get(id)
    # Check whether the post exists
    # if not return a 404 with a message
    if not post:
        return post_not_found(id)
        
    session.delete(post)
    session.commit()
    
    # Return the post as JSON
    data = message = "Post deleted {}".format(id)
    data = json.dumps({"message": message})
    return Response(data, 200, mimetype="application/json")
    
    
#     @app.route("/post/<int:id>/delete", methods =["GET"])
# def delete_post_get(id):
#     post = session.query(Post).get(id)
#     if post is None:
#         abort(404)
#     else:
#         if post.author_id == current_user.id:
#             session.delete(post)
#             session.commit()
#             return redirect(url_for("posts"))
#         else:
#             abort(403)
    
    
    
    ## old code from last blog - 
    # if post is None:
    #     abort(404)
    # else:
    #     if post.author_id == current_user.id:
    #         session.delete(post)
    #         session.commit()
    #         return redirect(url_for("posts"))
    #     else:
    #         abort(403)
    


        



from flask import render_template, redirect, url_for, flash, request, session, abort
from app import db
from . import post_bp
from .forms import PostForm
from .models import Post


@post_bp.route("/", methods=["GET"])
def all_posts():
    posts = db.session.query(Post).order_by(Post.posted.desc()).all()
    return render_template("posts/posts.html", posts=posts, page_title="Posts")


@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        author = session.get("user", "Anonymous")

        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            posted=form.publish_date.data,
            category=form.category.data,
        )

        if hasattr(new_post, "is_active"):
            new_post.is_active = bool(form.is_active.data)
        if hasattr(new_post, "author"):
            new_post.author = author

        db.session.add(new_post)
        db.session.commit()

        flash("Post added successfully", "success")
        return redirect(url_for("posts.all_posts"))

    if request.method == "POST":
        flash("Enter the correct data in the form!", "danger")

    return render_template("posts/add_post.html", form=form, page_title="Create Post")


@post_bp.route("/<int:id>", methods=["GET"])
def detail_post(id: int):
    post = db.session.get(Post, id)
    if not post:
        abort(404)
    return render_template("posts/detail_post.html", post=post, page_title=post.title)


@post_bp.route("/<int:id>/update", methods=["GET", "POST"])
def update_post(id: int):
    post = db.session.get(Post, id)
    if not post:
        abort(404)

    form = PostForm(obj=post)


    if request.method == "GET":
        if getattr(post, "posted", None):
            form.publish_date.data = post.posted

        if hasattr(post, "is_active"):
            form.is_active.data = bool(post.is_active)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.posted = form.publish_date.data

        if hasattr(post, "is_active"):
            post.is_active = bool(form.is_active.data)

        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for("posts.detail_post", id=post.id))

    if request.method == "POST":
        flash("Enter the correct data in the form!", "danger")

    return render_template("posts/add_post.html", form=form, page_title="Update Post")


@post_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id: int):
    post = db.session.get(Post, id)
    if not post:
        abort(404)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", "danger")
        return redirect(url_for("posts.all_posts"))

    return render_template("posts/delete_confirm.html", post=post, page_title="Delete Post")
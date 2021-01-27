# Pixelfield Test

This is a project to create an application using Django REST framework.

### Installation 

Install and run with docker and docker-compose->

```sh
$ docker-compose run web python manage.py loaddata ./wallet/fixture/data.json
$ sudo docker-compose up --build
```

Run directly through terminal->

```sh
$ sudo apt -y install postgresql-12 postgresql-client-12
$ sudo apt install postgis postgresql-12-postgis-3
$ sudo apt-get install postgresql-12-postgis-3-scripts
$ export ENGINE=django.contrib.gis.db.backends.postgis DB_NAME=pixelblog POSTGRES_USER=postgres POSTGRES_PASSWORD=saamiya DB_HOST=127.0.0.1 DB_PORT=5432 APP_PORT=8000 DJANGO_SU_NAME=admin DJANGO_SU_EMAIL=admin12@admin.com DJANGO_SU_PASSWORD=mypass123
$ pip install virtualenv
$ virtualenv env
$ source ./env/bin/activate
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py loaddata ./pixelblog/fixture/data.json
$ python manage.py runserver 127.0.0.1:8000
```
 user to create blog posts, categories, tags and users
Using this application the user can create blog posts, categories, tags, users and comments
C -> POST
R -> GET
U -> PUT
D -> DELETE

# API Queries
#### - Create a Category [POST]
```http
POST /api/v1/pixelblog/category
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `category_name` | `string` | **Required**. Category Name |
| `slug` | `string` | **Required**. Slug belonging to the post to which this category is attached |
#### - Create a Tag [POST]
```http
POST /api/v1/pixelblog/tag
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `tag_name` | `string` | **Required**. Tag Name |
| `slug` | `string` | **Required**. Slug belonging to the post to which this category is attached |
#### - CRUD a Blog [POST/PUT/GET/DELETE]
```http
POST /api/v1/pixelblog/blog
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `tags_names` | `list` | **Required**. Tags |
| `category_name` | `list` | **Required**. Categories |
| `slug` | `string` |  Slug |
| `title` | `string` | **Required**. Title of the blog |
| `author_name` | `string` | **Required**. Name of the author |

```http
GET /api/v1/pixelblog/blog
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `slug` | `string` |   **Required**. Slug |
| `title` | `string` | **Required**. Title of the blog |
| `author_name` | `string` | **Required**. Name of the author |

```http
PUT /api/v1/pixelblog/blog
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `tags_names` | `list` | **Required**. Tags |
| `category_name` | `list` | **Required**. Categories |
| `slug` | `string` |   **Required**. Slug |
| `title` | `string` | **Required**. Title of the blog |
| `author_name` | `string` | **Required**. Name of the author |

```http
DELETE /api/v1/pixelblog/blog
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `slug` | `string` |   **Required**. Slug |
| `title` | `string` | **Required**. Title of the blog |
| `author_name` | `string` | **Required**. Name of the author |

#### - CRUD a User [POST/PUT/GET/DELETE]
```http
POST /api/v1/pixelblog/blog
```
```http
PUT /api/v1/pixelblog/blog
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `email` | `string` | **Required**. Email |
| `password` | `string` | **Required**. Password |
| `name` | `string` | **Required**. Name |
| `address` | `string` | **Required**. Address |

```http
GET /api/v1/pixelblog/blog
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `email` | `string` | **Required**. Email |
| `password` | `string` | **Required**. Password |
| `name` | `string` | **Required**. Name |
| `address` | `string` | **Required**. Address |
```javascript
{
'success':True,
'Users in 1 km radius':['a','b','v'],
"Status":"Please Enter Name and Email"
}
```
```http
DELETE /api/v1/pixelblog/blog
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `email` | `string` | **Required**. Email |
| `password` | `string` | **Required**. Password |
| `name` | `string` | **Required**. Name |
| `address` | `string` | **Required**. Address |

#### - Post a Comment or Delete a comment [POST/DELETE]
```http
POST /api/v1/pixelblog/blog
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `title` | `string` | **Required**. Blog Title |
| `comment` | `string` | **Required**. Comment |

```http
DELETE /api/v1/pixelblog/blog
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `title` | `string` | **Required**. Blog Title |
| `comment` | `string` | **Required**. Comment |

#### - Post Content of a Blog [GET/POST]
```http
POST /api/v1/pixelblog/blog
```
```http
GET /api/v1/pixelblog/blog
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `content` | `string` | **Required**. Blog Content |
| `title` | `string` | **Required**. Blog TItle |
| `slug` | `string` | Slug |




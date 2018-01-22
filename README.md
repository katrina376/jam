# Jam

A realtime online discussions management system for conferences. Powered by [Django](https://www.djangoproject.com/) and [Django REST Framework](http://www.django-rest-framework.org). Inspired by [sli.do](https://sli.do).

## Introdution

This is a web application for realtime online discussions for conferences or seminars. For every talk, the user can leave comments and reply to comments. In addition, the user can up-vote or down-vote the comments to change the showing order. Comments of the speakers of the talk will be highlighted.

## Modules

### Core

The core module of Jam. It manages components including:

1. Talks in a section.
2. Comments to a talk ("root comments"), and comments to another comment ("leaf comments").
3. Votes to a comment.

All of the components are related to the authentication user model by many-to-one or many-to-many relation. Hence, if the `account` module provided in Jam is not used, there must be another module for authentication installed. This can be configurated by setting `AUTH_USER_MODEL` to the full application label in `settings.py`.

The `section` module is optional. Only the talk model is related to the section model by many-to-one relation, and it is optional. This can be configurated by setting `SECTION_MODEL` to the full application label in `settings.py`.

### Section

The module which manages the components of section in a conference.

### Account

The module which manages the users.

## Setup

1. Add `core` to `INSTALLED_APPS` in `settings.py`.
2. Set `AUTH_USER_MODEL` in `settings.py` to the full application label of the user model used for authentication. Add the application to `INSTALLED_APPS`.
3. Set `SECTION_MODEL` in `settings.py` to the full application label of the section model. Add the application to `INSTALLED_APPS`.

# Jam
A realtime online discussions management system for conferences.


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
2. Set `AUTH_USER_MODEL` to the full application label of the user model used for authentication.
3. Set `SECTION_MODEL` to the full application label of the section model.

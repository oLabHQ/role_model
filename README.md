# Quickstart #

```
make install
make run
```

# Project Implementation Plan #
1. The current Makefile is relevant only for initial, local development before
   a team is involved. It ought to be replaced with better devops, such as
   using Docker, allowing creation of dev, test databases, and deployment to
   production; that would be more suitable for team development.

2. Build the Admin up.

3. Build the business logic.
    a. Ensure test coverage complete.
    b. Have a think about a file format for sharing and loading organization
       roles and responsibilities templates. E.g. a typical one for a software
       start up.

4. Add appropriate logging.

5. Make sure gettext translatable strings are marked.

6. Construct the API.

7. Add obvious indexes, default select_related to Query/Manager classes.

8. Build frontend.

9. Set up deployment procedures; separate settings per environment, etc.

10. Move modules to private PyPI server and introduce SemVer.

11. Ensure project is up to scratch.

12. Invite friends to join.

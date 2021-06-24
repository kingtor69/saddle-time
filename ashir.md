# SaddleTime
## Feedback from Ashir Amin
### 210624

 - using AJAX/Axios for API calls enables better async functionality for slow (as in free) APIs
 - I redit some routes to use more RESTful API stuff on my site, per his advice
 - I'm doing the right thing for this by using SQLAlchemy, but should keep in mind there are better, lighter ORMs that don't require you to build the whole ORM model over again after writing the schema in sql.
 - store a guest user in front end localStorage
 - also guest's route-in-process in localStorage
 - create the route on the front end and only use the SQLAlchemy object when saving it
 - google architecture question "where to store anonymous user data"
 - 
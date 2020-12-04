# Django Backend

## Points to be noted
1.  When you install **djongo** it automatically install **django version-3.0.5** which is not the latest version.
2. You should go to `site-packages/pymongo/mongo_client.py line-90` this location of your virtual env or on your system and edit the **HOST** variable value which is default as **localhost**.
3. This log was generated while using migration for the first time.
```Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, user
Running migrations:
This version of djongo does not support "NULL, NOT NULL column validation check" fully. Visit https://www.patreon.com/nesdis
  Applying contenttypes.0001_initial...This version of djongo does not support "schema validation using CONSTRAINT" fully. Visit https://www.patreon.com/nesdis
 OK
  Applying contenttypes.0002_remove_content_type_name...This version of djongo does not support "COLUMN DROP NOT NULL " fully. Visit https://www.patreon.com/nesdis
This version of djongo does not support "DROP CASCADE" fully. Visit https://www.patreon.com/nesdis
 OK
  Applying auth.0001_initial...This version of djongo does not support "schema validation using KEY" fully. Visit https://www.patreon.com/nesdis
This version of djongo does not support "schema validation using REFERENCES" fully. Visit https://www.patreon.com/nesdis
 OK
 ```

4. Environment Variables `USER_EMAIL` for Email and `USER_PASS` for email's password should be created on your system or the server where you deploy. It is done for the privacy purpose. It is best to do the same for django secret key.
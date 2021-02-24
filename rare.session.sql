INSERT INTO auth_user (
    id,
    password,
    last_login,
    is_superuser,
    username,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined,
    first_name
  )
VALUES (
    id:integer,
    'password:varchar(128)',
    'last_login:datetime',
    is_superuser:bool,
    'username:varchar(150)',
    'last_name:varchar(150)',
    'email:varchar(254)',
    is_staff:bool,
    is_active:bool,
    'date_joined:datetime',
    'first_name:varchar(150)'
  );

DELETE FROM rareapi_subscription WHERE id=1;

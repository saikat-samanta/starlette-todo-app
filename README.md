# starlette-todo-app

A todo app using `starlette` with uvicorn server and `react`. It has basic user authentication using JWT and CURD operation for todos in a in-memory JSON DB.

## Run app

### Change directory to frontend and install dependency

```sh
cd frontend
yarn install
yarn build
cd ..
```

### Rename `.env.example` file to `.env` (inside backend)

```sh
cd backend
pip install -r requirements.txt
uvicorn --reload main:app --port 3600
```

### Now visit

- For UI

  ```txt
  http://localhost:3600/
  ```

- For API
  ```txt
  http://api.localhost:3600/
  ```
